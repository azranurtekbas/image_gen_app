"""Video modelleri için merkezi tahmini maliyet hesaplayıcısı."""


def estimate_video_price(
    pricing: dict,
    resolution: str,
    duration: int,
    audio: bool = False,
    voice_control: bool = False,
    num_reference_images: int = 0,
    reference_video_duration: int = 0,
) -> dict:
    """Model pricing şemasına göre video üretiminin tahmini USD maliyetini döndürür."""
    total = None
    breakdown = "Fiyat hesaplanamadı"

    if "flat_per_second" in pricing:
        rate = pricing["flat_per_second"]["price_per_second"]
        total = rate * duration
        breakdown = f"{duration}sn x ${rate}"

    elif "audio_tiers_per_second" in pricing:
        tiers = pricing["audio_tiers_per_second"]
        tier_name = "voice control" if voice_control else ("ses açık" if audio else "ses kapalı")
        rate = tiers["voice_control"] if voice_control else tiers["audio_on"] if audio else tiers["audio_off"]
        total = rate * duration
        breakdown = f"{duration}sn x ${rate} ({tier_name})"

    elif "resolution_per_second" in pricing and resolution in pricing["resolution_per_second"]:
        rate = pricing["resolution_per_second"].get(resolution)
        if rate is not None:
            total = rate * duration
            breakdown = f"{duration}sn x ${rate} ({resolution})"

    elif "resolution_audio_per_second" in pricing:
        tier = pricing["resolution_audio_per_second"].get(resolution, {})
        tier_name = "audio_on" if audio else "audio_off"
        rate = tier.get(tier_name)
        if rate is not None:
            total = rate * duration
            breakdown = f"{duration}sn x ${rate} ({resolution}, {'ses açık' if audio else 'ses kapalı'})"

    elif "duration_base_plus_extra" in pricing:
        tier = pricing["duration_base_plus_extra"]
        extra_seconds = max(0, duration - tier["base_seconds"])
        total = tier["base_price"] + extra_seconds * tier["extra_per_second"]
        breakdown = f"${tier['base_price']} ({tier['base_seconds']}sn temel) + {extra_seconds}sn x ${tier['extra_per_second']}"

    elif "token_formula" in pricing:
        tier = pricing["token_formula"]
        pixels = tier["resolution_pixels"].get(resolution)
        prices = tier["token_price_per_1000"]
        price_per_1000 = (prices.get("with_audio" if audio else "without_audio") if isinstance(prices, dict) and {"with_audio", "without_audio"}.issubset(prices) else prices.get(resolution)) if isinstance(prices, dict) else prices
        if pixels and price_per_1000 is not None:
            width, height = pixels
            effective_duration = reference_video_duration + duration if reference_video_duration > 0 else duration
            tokens = (width * height * effective_duration * tier.get("fps", 24)) / 1024
            total = (tokens / 1000) * price_per_1000
            if reference_video_duration > 0 and tier.get("reference_video_multiplier") is not None:
                total *= tier["reference_video_multiplier"]
            breakdown = f"{effective_duration}sn, {resolution}, {round(tokens, 1)} token x ${price_per_1000}/1K"

    if total is None:
        return {"estimated_usd": None, "breakdown": "Fiyat hesaplanamadı", "unverified": True}

    extras = pricing.get("extra_charges", {})
    free_images = extras.get("free_reference_images", 0)
    reference_charge = max(0, num_reference_images - free_images) * extras.get("per_reference_image", 0)
    input_charge = extras.get("image_input_charge", 0)
    if reference_charge or input_charge:
        total += reference_charge + input_charge
        breakdown += f" + ${reference_charge + input_charge} ek ücret"

    return {
        "estimated_usd": round(total, 4),
        "breakdown": breakdown,
        "unverified": pricing.get("unverified", False),
    }
