"""Tahmini maliyetlerdir; gerçek fal.ai faturası modelin nihai çözünürlüğüne göre farklı olabilir."""

SIZE_TO_PIXELS = {
    "square_hd": (1024, 1024), "square": (512, 512), "portrait_4_3": (768, 1024),
    "portrait_16_9": (576, 1024), "landscape_4_3": (1024, 768), "landscape_16_9": (1024, 576),
    "1:1": (1024, 1024), "16:9": (1344, 756), "9:16": (756, 1344), "4:3": (1182, 886),
    "3:4": (886, 1182), "3:2": (1254, 836), "2:3": (836, 1254), "21:9": (1536, 658), "9:21": (658, 1536),
}

def infer_tier_from_size(size_value: str | None) -> str:
    if str(size_value).lower() in {"2k", "2048"}: return "2k"
    if str(size_value).lower() in {"4k", "4096"}: return "4k"
    width, height = SIZE_TO_PIXELS.get(size_value, (1024, 1024))
    longest = max(width, height)
    return "4k" if longest >= 3000 else "2k" if longest >= 1800 else "standard"

def estimate_price(model_config: dict, size_value: str | None, num_reference_images: int = 0, quality: str | None = None) -> dict:
    pricing = model_config.get("pricing", {})
    unit = pricing.get("unit")
    tier = infer_tier_from_size(size_value)
    selected_quality = quality or pricing.get("default_quality", "medium")
    amount = None
    if unit == "image": amount = pricing.get("price_per_image")
    elif unit == "tiered": amount = pricing.get("tiers", {}).get(tier, pricing.get("tiers", {}).get("standard"))
    elif unit == "quality_tiered": amount = pricing.get("qualities", {}).get(selected_quality)
    elif unit == "resolution_quality":
        amount = pricing.get("tiers", {}).get(tier, pricing.get("tiers", {}).get("standard", {})).get(selected_quality)
    elif unit == "output_input":
        output_cost = pricing.get("output_tiers", {}).get(tier, pricing.get("output_tiers", {}).get("standard"))
        amount = None if output_cost is None else output_cost + num_reference_images * pricing.get("input_per_image", 0)
    elif unit == "megapixel":
        width, height = SIZE_TO_PIXELS.get(size_value, (1024, 1024))
        amount = round(max(1, round(width * height / 1_000_000)) * pricing.get("price_per_mp", 0), 4)
    return {"estimated_usd": amount, "unit": unit, "tier": tier, "quality": selected_quality, "unverified": pricing.get("unverified", True), "is_estimate": True}
