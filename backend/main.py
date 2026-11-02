"""FastAPI sunucusu."""
import os
import tempfile
import time
import asyncio
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from uuid import UUID, uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field
from image_service import ImageGenerationError, generate_image
from models_registry import MODEL_REGISTRY
from pricing_calc import estimate_price
from video_models_registry import VIDEO_MODEL_REGISTRY
from video_pricing_calc import estimate_video_price
import fal_client

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
def writable_runtime_dir(name: str) -> Path:
    """Desktop koruması etkinse AppData altında güvenli yazılabilir klasöre düşer."""
    preferred = BACKEND_DIR / name
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return preferred
    except PermissionError:
        fallback = Path(tempfile.gettempdir()) / "AIImageStudio" / name
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

UPLOADS_DIR, OUTPUTS_DIR = writable_runtime_dir("uploads"), writable_runtime_dir("outputs")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
app = FastAPI(title="AI Görüntü Üretim API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class CustomModel(BaseModel):
    endpoint: str = Field(min_length=1, max_length=200)
    supports_reference: bool = False
    reference_param: str | None = "image_urls"
    reference_is_list: bool = True
    max_reference_images: int = Field(default=1, ge=1, le=14)
    size_param: str | None = None
    size_values: list[str] = []
    extra_params: dict = {}

class GenerateRequest(BaseModel):
    prompt: str
    model_id: str = "flux-2-pro"
    reference_file_id: str | None = None
    image_size: str | None = None
    custom_model: CustomModel | None = None

class GenerateVideoRequest(BaseModel):
    model_id: str
    prompt: str
    starting_image_file_id: str | None = None
    reference_file_ids: list[str] = Field(default_factory=list)
    resolution: str
    duration: int
    audio: bool = False
    voice_control: bool = False

def public_model(model: dict) -> dict:
    public={key: model.get(key) for key in ("id", "label", "category", "provider", "supports_reference", "size_param", "size_values", "max_reference_images", "unverified", "pricing")}
    default_size=(model.get("size_values") or [None])[0]
    public["estimated_usd_default"]=estimate_price(model,default_size).get("estimated_usd")
    return public

def resolve_model(request: GenerateRequest) -> dict:
    if request.model_id != "custom":
        model = MODEL_REGISTRY.get(request.model_id)
        if not model:
            raise HTTPException(400, "Bilinmeyen model_id. /api/models listesinden bir model seçin.")
        return model
    if not request.custom_model:
        raise HTTPException(400, "model_id='custom' için custom_model bilgisi gerekli.")
    model = request.custom_model.model_dump()
    if not model["endpoint"].startswith("fal-ai/"):
        raise HTTPException(400, "Endpoint ID 'fal-ai/' ile başlamalı.")
    if model["supports_reference"] and not model["reference_param"]:
        raise HTTPException(400, "Referans destekleyen özel model için reference_param gerekli.")
    model.update({"id": "custom", "label": "Özel model"})
    return model

@app.get("/api/health")
async def health_check() -> dict[str, str]: return {"status": "ok"}

@app.get("/api/models")
async def list_models() -> dict[str, list[dict]]:
    models = [public_model(model) for model in MODEL_REGISTRY.values()]
    return {
        "edit_models": [model for model in models if model["category"] == "edit"],
        "utility_models": [model for model in models if model["category"] == "utility"],
    }

@app.get("/api/estimate-price")
async def estimate_model_price(model_id: str, size_value: str | None = None, num_reference_images: int = 1, quality: str | None = None) -> dict:
    model=MODEL_REGISTRY.get(model_id)
    if not model: raise HTTPException(404,"Model bulunamadı.")
    return estimate_price(model, size_value, num_reference_images, quality)

def _validate_video_options(model: dict, resolution: str, duration: int) -> None:
    if resolution not in model["resolutions"]:
        raise HTTPException(400, f"Geçersiz çözünürlük. Geçerli değerler: {', '.join(model['resolutions'])}.")
    limits = model["duration"]
    if "fixed_options" in limits:
        if duration not in limits["fixed_options"]:
            raise HTTPException(400, f"Geçersiz süre. Geçerli değerler: {', '.join(map(str, limits['fixed_options']))} saniye.")
    elif duration < limits["min"] or duration > limits["max"] or (duration - limits["min"]) % limits.get("step", 1):
        raise HTTPException(400, f"Geçersiz süre. Geçerli aralık: {limits['min']}-{limits['max']} saniye (adım: {limits.get('step', 1)}).")

def _uploaded_path(file_id: str) -> Path:
    try:
        normalized = UUID(file_id).hex
    except ValueError as exc:
        raise HTTPException(422, "Referans görseli bulunamadı.") from exc
    matches = list(UPLOADS_DIR.glob(f"{normalized}.*"))
    if len(matches) != 1 or not matches[0].is_file():
        raise HTTPException(422, "Referans görseli bulunamadı.")
    return matches[0]

def _video_url_from_result(result: dict) -> str:
    if isinstance(result.get("video"), dict) and result["video"].get("url"):
        return result["video"]["url"]
    if result.get("video_url"):
        return result["video_url"]
    for value in result.values():
        if isinstance(value, dict) and value.get("url"):
            return value["url"]
    raise ImageGenerationError("Model yanıtında video URL'si bulunamadı", 422)

def _generate_video_sync(request: GenerateVideoRequest, model: dict, paths: list[Path]) -> str:
    try:
        urls = [fal_client.upload_file(str(path)) for path in paths]
        arguments = {"prompt": request.prompt, "resolution": request.resolution, "duration": request.duration}
        if model["input_mode"] == "image_to_video":
            arguments["image_url"] = urls[0]
        else:
            arguments["image_urls"] = urls
        if model["supports_audio"]:
            arguments["generate_audio"] = request.audio
        if model["supports_voice_control"] and request.voice_control:
            arguments["voice_control"] = True
        result = fal_client.subscribe(model["endpoint"], arguments=arguments, with_logs=True)
        video_url = _video_url_from_result(result)
        data = urlopen(Request(video_url, headers={"User-Agent": "image-gen-app/1.0"}), timeout=180).read()
        if not data:
            raise ImageGenerationError("Üretilen video indirilemedi")
        filename = f"{uuid4().hex}.mp4"
        (OUTPUTS_DIR / filename).write_bytes(data)
        return f"/outputs/{filename}"
    except ImageGenerationError:
        raise
    except Exception as exc:
        detail = str(exc).lower()
        if any(key in detail for key in ("401", "unauthorized", "invalid key")):
            raise ImageGenerationError("API anahtarı geçersiz", 401) from exc
        if any(key in detail for key in ("429", "rate limit", "too many requests")):
            raise ImageGenerationError("İstek limiti aşıldı, lütfen birazdan tekrar deneyin", 429) from exc
        if any(key in detail for key in ("404", "path", "not found")):
            raise ImageGenerationError(f"Video endpoint bulunamadı veya erişilemiyor: {str(exc)[:500]}", 422) from exc
        if any(key in detail for key in ("422", "validation", "invalid input", "content policy", "safety", "literal_error", "input should")):
            raise ImageGenerationError(f"Video modeli doğrulama hatası: {str(exc)[:500]}", 422) from exc
        raise ImageGenerationError(f"Video üretilemedi: {str(exc)[:500]}") from exc

@app.get("/api/video-models")
async def list_video_models() -> list[dict]:
    fields = ("id", "label", "provider", "input_mode", "supports_audio", "supports_voice_control", "resolutions", "duration", "max_reference_images", "pricing")
    return [{field: model[field] for field in fields} for model in VIDEO_MODEL_REGISTRY.values()]

@app.get("/api/estimate-video-price")
async def estimate_video_model_price(model_id: str, resolution: str, duration: int, audio: bool = False, voice_control: bool = False, num_references: int = 0, reference_video_duration: int = 0) -> dict:
    model = VIDEO_MODEL_REGISTRY.get(model_id)
    if not model:
        raise HTTPException(404, "Video modeli bulunamadı.")
    _validate_video_options(model, resolution, duration)
    return estimate_video_price(model["pricing"], resolution, duration, audio, voice_control, num_references, reference_video_duration)

@app.post("/api/generate-video")
async def generate_video(request: GenerateVideoRequest) -> dict:
    model = VIDEO_MODEL_REGISTRY.get(request.model_id)
    if not model:
        raise HTTPException(404, "Video modeli bulunamadı.")
    _validate_video_options(model, request.resolution, request.duration)
    if request.audio and not model["supports_audio"]:
        raise HTTPException(400, "Seçilen video modeli ses üretimini desteklemiyor.")
    if request.voice_control and not model["supports_voice_control"]:
        raise HTTPException(400, "Seçilen video modeli voice control desteklemiyor.")
    if model["input_mode"] == "image_to_video":
        if not request.starting_image_file_id:
            raise HTTPException(400, "Bu model için starting_image_file_id gerekli.")
        paths = [_uploaded_path(request.starting_image_file_id)]
    else:
        if not request.reference_file_ids:
            raise HTTPException(400, "Bu model için reference_file_ids gerekli.")
        if len(request.reference_file_ids) > model["max_reference_images"]:
            raise HTTPException(400, f"Bu model en fazla {model['max_reference_images']} referans kabul eder.")
        paths = [_uploaded_path(file_id) for file_id in request.reference_file_ids]
    estimated_cost = estimate_video_price(model["pricing"], request.resolution, request.duration, request.audio, request.voice_control, len(paths))
    started_at = time.time()
    try:
        output_url = await asyncio.to_thread(_generate_video_sync, request, model, paths)
    except ImageGenerationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from exc
    return {"output_url": output_url, "generation_time_seconds": round(time.time() - started_at, 2), "estimated_cost": estimated_cost}

@app.post("/api/generate")
async def generate(request: GenerateRequest) -> dict[str, str]:
    model = resolve_model(request)
    if request.image_size and model.get("size_param") and model.get("size_values") and request.image_size not in model.get("size_values", []):
        raise HTTPException(400, f"Bu model için geçersiz boyut/oran. Geçerli değerler: {', '.join(model.get('size_values', []))}.")
    references = None
    if request.reference_file_id:
        if not model.get("supports_reference"):
            raise HTTPException(400, "Seçilen model referans görsel desteklemiyor.")
        try: file_id = UUID(request.reference_file_id).hex
        except ValueError as exc: raise HTTPException(422, "Referans görseli bulunamadı.") from exc
        matches = list(UPLOADS_DIR.glob(f"{file_id}.*"))
        if len(matches) != 1 or not matches[0].is_file(): raise HTTPException(422, "Referans görseli bulunamadı.")
        references = [str(matches[0])]
    try:
        return {"output_url": await generate_image(request.prompt, model, references, request.image_size)}
    except ImageGenerationError as exc:
        raise HTTPException(exc.status_code, str(exc)) from exc

@app.post("/api/upload-reference")
async def upload_reference(file: UploadFile = File(...)) -> dict[str, str]:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS: raise HTTPException(400, f"Desteklenmeyen uzantı. İzin verilen: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}.")
    saved_path = None
    try:
        content = await file.read(MAX_UPLOAD_SIZE + 1)
        if len(content) > MAX_UPLOAD_SIZE: raise HTTPException(413, "Dosya boyutu 10 MB sınırını aşıyor.")
        file_id = uuid4().hex; filename = f"{file_id}{extension}"; saved_path = UPLOADS_DIR / filename; saved_path.write_bytes(content)
        try:
            with Image.open(BytesIO(content)) as image: image.verify()
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            saved_path.unlink(missing_ok=True); raise HTTPException(400, "Yüklenen dosya geçerli bir görüntü değil veya bozuk.") from exc
        return {"file_id": file_id, "filename": filename, "url": f"/uploads/{filename}"}
    except HTTPException: raise
    except PermissionError as exc: raise HTTPException(500, "Yükleme klasörüne yazma izni yok.") from exc
    except OSError as exc:
        if saved_path: saved_path.unlink(missing_ok=True)
        raise HTTPException(500, f"Dosya kaydedilemedi: {exc}") from exc
    finally: await file.close()

@app.get("/", include_in_schema=False)
async def index() -> FileResponse: return FileResponse(FRONTEND_DIR / "index.html")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
