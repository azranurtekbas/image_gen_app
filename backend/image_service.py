"""Kayıt defterindeki veya özel fal.ai modelleri ile üretim."""
import asyncio
import mimetypes
import os
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

# Bu geliştirme ortamında proxy değişkenleri kapalı bir localhost portuna işaret ediyor.
# fal.ai istekleri doğrudan internete çıkmalıdır.
for _proxy_var in ("ALL_PROXY", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "http_proxy", "https_proxy"):
    os.environ.pop(_proxy_var, None)

import fal_client
import config

# Windows korumalı klasörleri Python yazımını engelleyebildiği için main.py ile aynı çalışma alanı.
OUTPUTS_DIR = Path(tempfile.gettempdir()) / "AIImageStudio" / "outputs"

class ImageGenerationError(Exception):
    def __init__(self, message: str, status_code: int = 500): super().__init__(message); self.status_code = status_code

def _require_fal_key():
    if not config.FAL_KEY: raise ImageGenerationError("FAL_KEY .env dosyasında tanımlı değil")

def _service_error(exc: Exception) -> ImageGenerationError:
    detail, lowered = str(exc), str(exc).lower()
    if any(v in lowered for v in ("404", "not found", "endpoint")): return ImageGenerationError("Bu endpoint bulunamadı, ID'yi kontrol et", 422)
    if any(v in lowered for v in ("401", "unauthorized", "invalid key", "authentication")): return ImageGenerationError("API anahtarı geçersiz", 401)
    if any(v in lowered for v in ("429", "rate limit", "too many requests")): return ImageGenerationError("İstek limiti aşıldı, lütfen birazdan tekrar deneyin", 429)
    if getattr(exc, "status_code", None) in (400, 422): return ImageGenerationError(f"Model doğrulama hatası: {detail}", 422)
    if any(v in lowered for v in ("validation", "unprocessable", "422", "invalid input")): return ImageGenerationError(f"Model doğrulama hatası: {detail}", 422)
    if any(v in lowered for v in ("content policy", "safety", "moderation")): return ImageGenerationError("Görsel üretilemedi, farklı bir prompt deneyin", 422)
    # fal.ai, yanlış endpoint/parametre veya kota gibi durumlarda ayrıntıyı burada verir.
    safe_detail = detail[:500] if detail else "Bilinmeyen servis hatası"
    return ImageGenerationError(f"Görsel üretilemedi: {safe_detail}", 500)

def _extension(content_type: str | None) -> str:
    value = mimetypes.guess_extension((content_type or "").split(";", 1)[0])
    return value if value in {".jpg", ".jpeg", ".png", ".webp"} else ".png"

def _generate_sync(prompt: str, model_config: dict, reference_paths: list[str] | None, size_value: str | None) -> str:
    _require_fal_key(); arguments = {"prompt": prompt}
    try:
        if reference_paths and model_config.get("supports_reference"):
            paths = reference_paths[:model_config.get("max_reference_images", 1)]
            urls = [fal_client.upload_file(path) for path in paths]
            key = model_config["reference_param"]
            arguments[key] = urls if model_config.get("reference_is_list") else urls[0]
            endpoint = model_config.get("edit_endpoint") or model_config["endpoint"]
        else: endpoint = model_config["endpoint"]
        if size_value and model_config.get("size_param") and not (reference_paths and model_config.get("reference_disables_size")):
            arguments[model_config["size_param"]] = size_value
        arguments.update(model_config.get("extra_params", {}))
        result = fal_client.subscribe(endpoint, arguments=arguments, with_logs=True)
        image_url = result["images"][0]["url"]
    except ImageGenerationError: raise
    except (KeyError, IndexError, TypeError) as exc: raise ImageGenerationError("Model yanıtında görsel URL'si bulunamadı", 422) from exc
    except Exception as exc: raise _service_error(exc) from exc
    try:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        with urlopen(Request(image_url, headers={"User-Agent": "image-gen-app/1.0"}), timeout=60) as response:
            data = response.read(); suffix = _extension(response.headers.get_content_type())
        if not data: raise ImageGenerationError("Üretilen görsel indirilemedi")
        filename = f"{uuid4().hex}{suffix}"; (OUTPUTS_DIR / filename).write_bytes(data)
        return f"/outputs/{filename}"
    except ImageGenerationError: raise
    except HTTPError as exc: raise ImageGenerationError("Üretilen görsel indirilemedi") from exc
    except URLError as exc: raise ImageGenerationError("Görsel indirilirken ağ hatası oluştu") from exc
    except OSError as exc: raise ImageGenerationError("Görsel kaydedilemedi; disk alanını ve izinleri kontrol edin") from exc

async def generate_image(prompt: str, model_config: dict, reference_paths: list[str] | None = None, size_value: str | None = None) -> str:
    if not prompt.strip(): raise ImageGenerationError("Prompt boş olamaz", 422)
    return await asyncio.to_thread(_generate_sync, prompt, model_config, reference_paths, size_value)
