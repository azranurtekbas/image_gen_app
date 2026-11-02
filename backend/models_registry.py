"""fal.ai model kataloğu; sıralama kullanıcı tarafından sağlanan favori sırasıdır."""

IMAGE_SIZES = ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"]
ASPECT_RATIOS = ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"]

def edit(id, label, endpoint, provider, reference_param="image_urls", reference_is_list=True, max_reference_images=1, size_param=None, size_values=None, unverified=True, pricing=None, **extra):
    return {"id": id, "label": label, "endpoint": endpoint, "category": "edit", "provider": provider, "supports_reference": True, "reference_param": reference_param, "reference_is_list": reference_is_list, "max_reference_images": max_reference_images, "size_param": size_param, "size_values": size_values or [], "extra_params": {}, "unverified": unverified, "pricing": pricing or {"unit": None, "unverified": True}, **extra}

def utility(id, label, endpoint, provider, pricing=None, **extra):
    return {"id": id, "label": label, "endpoint": endpoint, "category": "utility", "provider": provider, "supports_reference": False, "reference_param": None, "reference_is_list": False, "max_reference_images": 1, "size_param": None, "size_values": [], "extra_params": {}, "unverified": True, "pricing": pricing or {"unit": None, "unverified": True}, **extra}

MODEL_REGISTRY = {
    "nano-banana-2": edit("nano-banana-2", "Nano Banana 2 (Google)", "fal-ai/nano-banana-2/edit", "Google", max_reference_images=14, size_param="aspect_ratio", size_values=ASPECT_RATIOS, unverified=False, pricing={"unit":"tiered","tiers":{"standard":0.08,"2k":0.12,"4k":0.16},"unverified":False}),
    "nano-banana-pro": edit("nano-banana-pro", "Nano Banana Pro (Google)", "fal-ai/nano-banana-pro/edit", "Google"),
    "gpt-image-2": edit("gpt-image-2", "GPT Image 2 (OpenAI)", "openai/gpt-image-2/edit", "OpenAI"),
    "nano-banana": edit("nano-banana", "Nano Banana (Google)", "fal-ai/nano-banana/edit", "Google"),
    "seedream-v5-pro": edit("seedream-v5-pro", "Seedream V5 Pro (ByteDance)", "fal-ai/bytedance/seedream/v5/pro/edit", "ByteDance", max_reference_images=10),
    "birefnet-v2": utility("birefnet-v2", "BiRefNet V2 (fal.ai)", "fal-ai/birefnet/v2", "fal.ai"),
    "flux-kontext-pro": edit("flux-kontext-pro", "FLUX Kontext Pro (Black Forest Labs)", "fal-ai/flux-pro/kontext", "Black Forest Labs"),
    "seedream-v4.5": edit("seedream-v4.5", "Seedream V4.5 (ByteDance)", "fal-ai/bytedance/seedream/v4.5/edit", "ByteDance", max_reference_images=10, size_param="image_size", size_values=IMAGE_SIZES, unverified=False, pricing={"unit":"image","price_per_image":0.04,"unverified":False}),
    "seedvr-upscale": utility("seedvr-upscale", "SeedVR Upscale (fal.ai)", "fal-ai/seedvr/upscale/image", "fal.ai", extra_params={"scale": 2}),
    "flux-2-pro": edit("flux-2-pro", "FLUX.2 Pro (Black Forest Labs)", "fal-ai/flux-2-pro/edit", "Black Forest Labs", size_param="image_size", size_values=IMAGE_SIZES, unverified=False),
    "bria-rmbg": utility("bria-rmbg", "Bria Background Removal (Bria AI)", "bria/background/remove", "Bria AI"),
    "grok-imagine-edit": edit("grok-imagine-edit", "Grok Imagine Edit (xAI)", "xai/grok-imagine-image/edit", "xAI"),
    "clarity-upscaler": utility("clarity-upscaler", "Clarity Upscaler (fal.ai)", "fal-ai/clarity-upscaler", "fal.ai"),
    "seedream-v4": edit("seedream-v4", "Seedream V4 (ByteDance)", "fal-ai/bytedance/seedream/v4/edit", "ByteDance"),
    "nano-banana-lite": edit("nano-banana-lite", "Nano Banana Lite (Google)", "google/nano-banana-lite/edit", "Google", max_reference_images=14, size_param="aspect_ratio", size_values=ASPECT_RATIOS),
    "gemini-3-pro-image": edit("gemini-3-pro-image", "Gemini 3 Pro Image (Google)", "fal-ai/gemini-3-pro-image-preview/edit", "Google"),
    "esrgan": utility("esrgan", "ESRGAN Upscale (fal.ai)", "fal-ai/esrgan", "fal.ai", extra_params={"scale": 2}),
    "birefnet": utility("birefnet", "BiRefNet (fal.ai)", "fal-ai/birefnet", "fal.ai"),
    "grok-imagine-v2": edit("grok-imagine-v2", "Grok Imagine V2 (xAI)", "xai/grok-imagine-image/v2.0/edit", "xAI"),
    "nano-banana-flash": edit("nano-banana-flash", "Nano Banana Flash (Google)", "fal-ai/gemini-25-flash-image/edit", "Google"),
    "sam-3": utility("sam-3", "SAM 3 Segmentasyon (fal.ai)", "fal-ai/sam-3/image", "fal.ai"),
    "gpt-image-1.5": edit("gpt-image-1.5", "GPT Image 1.5 (OpenAI)", "fal-ai/gpt-image-1.5/edit", "OpenAI"),
    "flux-2-klein-9b": edit("flux-2-klein-9b", "FLUX.2 Klein 9B (Black Forest Labs)", "fal-ai/flux-2/klein/9b/edit", "Black Forest Labs"),
    "rembg": utility("rembg", "Rembg Background Removal (fal.ai)", "fal-ai/imageutils/rembg", "fal.ai"),
    "flux-dev-i2i": edit("flux-dev-i2i", "FLUX Dev Image-to-Image (Black Forest Labs)", "fal-ai/flux/dev/image-to-image", "Black Forest Labs", reference_param="image_url", reference_is_list=False, size_param="image_size", size_values=IMAGE_SIZES, unverified=False, pricing={"unit":"megapixel","price_per_mp":0.03,"unverified":False}),
    "flux-2-edit": edit("flux-2-edit", "FLUX.2 Edit (Black Forest Labs)", "fal-ai/flux-2/edit", "Black Forest Labs"),
    "flux-pro-fill": utility("flux-pro-fill", "FLUX Pro Fill (Black Forest Labs)", "fal-ai/flux-pro/v1/fill", "Black Forest Labs"),
    "aura-sr": utility("aura-sr", "Aura SR Upscale (fal.ai)", "fal-ai/aura-sr", "fal.ai"),
}

# Kullanıcının sağladığı 1024×1024 / 1K bazındaki fiyatlar.
# quality_tiered ve resolution_quality değerleri API üzerinden quality parametresiyle seçilebilir.
PRICING = {
    "nano-banana-2": {"unit": "tiered", "tiers": {"standard": .08, "2k": .12, "4k": .16}, "unverified": False},
    "nano-banana-pro": {"unit": "image", "price_per_image": .15, "unverified": False},
    "gpt-image-2": {"unit": "quality_tiered", "qualities": {"low": .011, "medium": .04, "high": .16}, "default_quality": "medium", "unverified": False},
    "nano-banana": {"unit": "image", "price_per_image": .04, "unverified": False},
    "seedream-v5-pro": {"unit": "tiered", "tiers": {"standard": .0675, "2k": .135}, "unverified": False},
    "birefnet-v2": {"unit": "image", "price_per_image": .015, "unverified": False},
    "flux-kontext-pro": {"unit": "image", "price_per_image": .04, "unverified": False},
    "seedream-v4.5": {"unit": "image", "price_per_image": .035, "unverified": False},
    "seedvr-upscale": {"unit": "image", "price_per_image": .02, "unverified": False},
    "flux-2-pro": {"unit": "image", "price_per_image": .073, "unverified": False},
    "bria-rmbg": {"unit": "image", "price_per_image": .02, "unverified": False},
    "grok-imagine-edit": {"unit": "output_input", "output_tiers": {"standard": .05, "2k": .07}, "input_per_image": .01, "unverified": False},
    "clarity-upscaler": {"unit": "image", "price_per_image": .031, "unverified": False},
    "seedream-v4": {"unit": "image", "price_per_image": .03, "unverified": False},
    "nano-banana-lite": {"unit": "image", "price_per_image": .025, "unverified": False},
    "gemini-3-pro-image": {"unit": "image", "price_per_image": .15, "unverified": False},
    "esrgan": {"unit": "image", "price_per_image": .008, "unverified": False},
    "birefnet": {"unit": "image", "price_per_image": .01, "unverified": False},
    "grok-imagine-v2": {"unit": "resolution_quality", "tiers": {"standard": {"low": .04, "medium": .06}, "2k": {"low": .06, "medium": .08}}, "default_quality": "medium", "unverified": False},
    "nano-banana-flash": {"unit": "image", "price_per_image": .04, "unverified": False},
    "sam-3": {"unit": "image", "price_per_image": .01, "unverified": False},
    "gpt-image-1.5": {"unit": "quality_tiered", "qualities": {"low": .009, "medium": .034, "high": .133}, "default_quality": "medium", "input_text_per_1k": .005, "output_text_per_1k": .01, "unverified": False},
    "flux-2-klein-9b": {"unit": "megapixel", "price_per_mp": .006, "unverified": False},
    "rembg": {"unit": "image", "price_per_image": .003, "unverified": False},
    "flux-dev-i2i": {"unit": "image", "price_per_image": .03, "unverified": False},
    "flux-2-edit": {"unit": "megapixel", "price_per_mp": .024, "input_price_per_mp": .012, "output_price_per_mp": .012, "unverified": False},
    "flux-pro-fill": {"unit": "megapixel", "price_per_mp": .05, "unverified": False},
    "aura-sr": {"unit": "image", "price_per_image": .015, "unverified": False},
}

for _model_id, _pricing in PRICING.items():
    MODEL_REGISTRY[_model_id]["pricing"] = _pricing
