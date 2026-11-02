"""Video model kataloğu; ekleme sırası kullanıcı arayüzündeki popülerlik sırasıdır."""

VIDEO_MODEL_REGISTRY = {
    "kling-v3-pro": {
        "id": "kling-v3-pro", "label": "Kling 3 Pro (Image to Video)", "endpoint": "fal-ai/kling-video/v3/pro/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": True, "resolutions": ["720p", "1080p"],
        "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.112, "audio_on": 0.168, "voice_control": 0.196}},
    },
    "seedance-2.5-i2v": {
        "id": "seedance-2.5-i2v", "label": "Seedance 2.5 (Image to Video)", "endpoint": "fal-ai/bytedance/seedance-2.5/image-to-video", "provider": "ByteDance",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p", "1080p"],
        "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"480p": 0.2205, "720p": 0.4730}, "token_formula": {"token_price_per_1000": {"1080p": 0.0234}, "fps": 24, "resolution_pixels": {"1080p": [1920, 1080]}}},
    },
    "kling-v2.5-turbo-pro": {
        "id": "kling-v2.5-turbo-pro", "label": "Kling 2.5 Turbo Pro (Image to Video)", "endpoint": "fal-ai/kling-video/v2.5-turbo/pro/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"],
        "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"duration_base_plus_extra": {"base_seconds": 5, "base_price": 0.35, "extra_per_second": 0.07}},
    },
    "seedance-2.0-i2v": {
        "id": "seedance-2.0-i2v", "label": "Seedance 2.0 (Image to Video)", "endpoint": "fal-ai/bytedance/seedance-2.0/image-to-video", "provider": "ByteDance",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p", "1080p", "4k"],
        "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"720p": 0.3034, "1080p": 0.682}, "token_formula": {"token_price_per_1000": {"480p": 0.014, "720p": 0.014, "1080p": 0.014, "4k": 0.008}, "fps": 24, "resolution_pixels": {"480p": [854, 480], "720p": [1280, 720], "1080p": [1920, 1080], "4k": [3840, 2160]}}},
    },
    "kling-v3-standard": {
        "id": "kling-v3-standard", "label": "Kling 3 Standard (Image to Video)", "endpoint": "fal-ai/kling-video/v3/standard/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": True, "resolutions": ["720p", "1080p"],
        "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.084, "audio_on": 0.126, "voice_control": 0.154}},
    },
    "kling-v2.6-pro": {
        "id": "kling-v2.6-pro", "label": "Kling 2.6 Pro (Image to Video)", "endpoint": "fal-ai/kling-video/v2.6/pro/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": True, "resolutions": ["720p", "1080p"],
        "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.07, "audio_on": 0.14, "voice_control": 0.168}},
    },
    "minimax-h3-i2v": {
        "id": "minimax-h3-i2v", "label": "MiniMax H3 (Image to Video)", "endpoint": "fal-ai/minimax/h3/image-to-video", "provider": "MiniMax",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "768p", "2k", "4k"],
        "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"480p": 0.05, "768p": 0.06, "2k": 0.13, "4k": 0.16}},
    },
    "veo3.1-fast-i2v": {
        "id": "veo3.1-fast-i2v", "label": "Veo 3.1 Fast (Image to Video)", "endpoint": "fal-ai/veo3.1/fast/image-to-video", "provider": "Google",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p", "1080p", "4k"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"resolution_audio_per_second": {"720p": {"audio_off": 0.10, "audio_on": 0.15}, "1080p": {"audio_off": 0.10, "audio_on": 0.15}, "4k": {"audio_off": 0.30, "audio_on": 0.35}}},
    },
    "grok-imagine-i2v": {
        "id": "grok-imagine-i2v", "label": "Grok Imagine (Image to Video)", "endpoint": "xai/grok-imagine-video/image-to-video", "provider": "xAI",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p"], "duration": {"min": 2, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"480p": 0.05, "720p": 0.07}, "extra_charges": {"image_input_charge": 0.002}},
    },
    "seedance-1.5-pro-i2v": {
        "id": "seedance-1.5-pro-i2v", "label": "Seedance 1.5 Pro (Image to Video)", "endpoint": "fal-ai/bytedance/seedance/v1.5/pro/image-to-video", "provider": "ByteDance",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"token_formula": {"token_price_per_1000": {"with_audio": 0.0024, "without_audio": 0.0012}, "fps": 24, "resolution_pixels": {"720p": [1280, 720]}}},
    },
    "veo3.1-i2v": {
        "id": "veo3.1-i2v", "label": "Veo 3.1 (Image to Video)", "endpoint": "fal-ai/veo3.1/image-to-video", "provider": "Google",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p", "1080p", "4k"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"resolution_audio_per_second": {"720p": {"audio_off": 0.20, "audio_on": 0.40}, "1080p": {"audio_off": 0.20, "audio_on": 0.40}, "4k": {"audio_off": 0.40, "audio_on": 0.60}}},
    },
    "kling-v2.1-standard": {
        "id": "kling-v2.1-standard", "label": "Kling 2.1 Standard (Image to Video)", "endpoint": "fal-ai/kling-video/v2.1/standard/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"duration_base_plus_extra": {"base_seconds": 5, "base_price": 0.28, "extra_per_second": 0.056}},
    },
    "grok-imagine-v1.5-i2v": {
        "id": "grok-imagine-v1.5-i2v", "label": "Grok Imagine 1.5 (Image to Video)", "endpoint": "xai/grok-imagine-video/v1.5/image-to-video", "provider": "xAI",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p", "1080p"], "duration": {"min": 2, "max": 10, "step": 1}, "max_reference_images": 7,
        "pricing": {"resolution_per_second": {"480p": 0.08, "720p": 0.14, "1080p": 0.25}, "extra_charges": {"per_reference_image": 0.01, "free_reference_images": 0}},
    },
    "seedance-2.0-fast-i2v": {
        "id": "seedance-2.0-fast-i2v", "label": "Seedance 2.0 Fast (Image to Video)", "endpoint": "fal-ai/bytedance/seedance-2.0/fast/image-to-video", "provider": "ByteDance",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"720p": 0.2419}, "token_formula": {"token_price_per_1000": 0.0112, "fps": 24, "resolution_pixels": {"720p": [1280, 720]}}},
    },
    "flux3-i2v": {
        "id": "flux3-i2v", "label": "FLUX.3 (Image to Video)", "endpoint": "blackforestlabs/flux-3/image-to-video", "provider": "Black Forest Labs",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"min": 3, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"720p": 0.17, "1080p": 0.29}},
    },
    "veo3.1-lite-i2v": {
        "id": "veo3.1-lite-i2v", "label": "Veo 3.1 Lite (Image to Video)", "endpoint": "fal-ai/veo3.1/lite/image-to-video", "provider": "Google",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"fixed_options": [4, 8]}, "max_reference_images": 1,
        "pricing": {"resolution_audio_per_second": {"720p": {"audio_off": 0.03, "audio_on": 0.05}, "1080p": {"audio_off": 0.05, "audio_on": 0.08}}},
    },
    "seedance-1-pro-i2v": {
        "id": "seedance-1-pro-i2v", "label": "Seedance 1.0 Pro (Image to Video)", "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video", "provider": "ByteDance",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"token_formula": {"token_price_per_1000": 0.0025, "fps": 24, "resolution_pixels": {"720p": [1280, 720], "1080p": [1920, 1080]}}},
    },
    "gemini-omni-flash-i2v": {
        "id": "gemini-omni-flash-i2v", "label": "Gemini Omni Flash (Image to Video)", "endpoint": "google/gemini-omni-flash/image-to-video", "provider": "Google",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"min": 2, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"720p": 0.13}, "unverified": True},
    },
    "kling-o3-pro": {
        "id": "kling-o3-pro", "label": "Kling O3 Pro (Image to Video)", "endpoint": "fal-ai/kling-video/o3/pro/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.112, "audio_on": 0.14}},
    },
    "kling-o3-standard": {
        "id": "kling-o3-standard", "label": "Kling O3 Standard (Image to Video)", "endpoint": "fal-ai/kling-video/o3/standard/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.084, "audio_on": 0.112}},
    },
    "wan-v2.7-i2v": {
        "id": "wan-v2.7-i2v", "label": "Wan 2.7 (Image to Video)", "endpoint": "fal-ai/wan/v2.7/image-to-video", "provider": "Wan",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"min": 3, "max": 10, "step": 1}, "max_reference_images": 1,
        "pricing": {"resolution_per_second": {"720p": 0.10, "1080p": 0.15}},
    },
    "gemini-omni-flash-ref": {
        "id": "gemini-omni-flash-ref", "label": "Gemini Omni Flash (Reference to Video)", "endpoint": "google/gemini-omni-flash/reference-to-video", "provider": "Google",
        "input_mode": "reference_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"min": 2, "max": 10, "step": 1}, "max_reference_images": 3,
        "pricing": {"resolution_per_second": {"720p": 0.13}, "unverified": True},
    },
    "kling-v3-turbo-pro": {
        "id": "kling-v3-turbo-pro", "label": "Kling 3 Turbo Pro (Image to Video)", "endpoint": "fal-ai/kling-video/v3/turbo/pro/image-to-video", "provider": "Kling",
        "input_mode": "image_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 1,
        "pricing": {"flat_per_second": {"price_per_second": 0.14}},
    },
    "kling-o3-pro-ref": {
        "id": "kling-o3-pro-ref", "label": "Kling O3 Pro (Reference to Video)", "endpoint": "fal-ai/kling-video/o3/pro/reference-to-video", "provider": "Kling",
        "input_mode": "reference_to_video", "supports_audio": True, "supports_voice_control": False, "resolutions": ["720p", "1080p"], "duration": {"fixed_options": [5, 10]}, "max_reference_images": 4,
        "pricing": {"audio_tiers_per_second": {"audio_off": 0.112, "audio_on": 0.14}},
    },
    "seedance-2.5-ref": {
        "id": "seedance-2.5-ref", "label": "Seedance 2.5 (Reference to Video)", "endpoint": "fal-ai/bytedance/seedance-2.5/reference-to-video", "provider": "ByteDance",
        "input_mode": "reference_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p", "1080p"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 4,
        "pricing": {"resolution_per_second": {"480p": 0.2205, "720p": 0.4730}, "token_formula": {"token_price_per_1000": {"1080p": 0.0234}, "fps": 24, "resolution_pixels": {"1080p": [1920, 1080]}, "reference_video_multiplier": 0.6}},
    },
    "seedance-2.0-ref": {
        "id": "seedance-2.0-ref", "label": "Seedance 2.0 (Reference to Video)", "endpoint": "fal-ai/bytedance/seedance-2.0/reference-to-video", "provider": "ByteDance",
        "input_mode": "reference_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "720p", "1080p", "4k"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 4,
        "pricing": {"resolution_per_second": {"720p": 0.3034, "1080p": 0.682}, "token_formula": {"token_price_per_1000": {"480p": 0.014, "720p": 0.014, "1080p": 0.014, "4k": 0.008}, "fps": 24, "resolution_pixels": {"480p": [854, 480], "720p": [1280, 720], "1080p": [1920, 1080], "4k": [3840, 2160]}, "reference_video_multiplier": 0.6}},
    },
    "seedance-2.0-fast-ref": {
        "id": "seedance-2.0-fast-ref", "label": "Seedance 2.0 Fast (Reference to Video)", "endpoint": "fal-ai/bytedance/seedance-2.0/fast/reference-to-video", "provider": "ByteDance",
        "input_mode": "reference_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["720p"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 4,
        "pricing": {"resolution_per_second": {"720p": 0.2419}, "token_formula": {"token_price_per_1000": 0.0112, "fps": 24, "resolution_pixels": {"720p": [1280, 720]}, "reference_video_multiplier": 0.6}},
    },
    "minimax-h3-ref": {
        "id": "minimax-h3-ref", "label": "MiniMax H3 (Reference to Video)", "endpoint": "fal-ai/minimax/h3/reference-to-video", "provider": "MiniMax",
        "input_mode": "reference_to_video", "supports_audio": False, "supports_voice_control": False, "resolutions": ["480p", "768p", "2k", "4k"], "duration": {"min": 5, "max": 10, "step": 1}, "max_reference_images": 10,
        "pricing": {"resolution_per_second": {"480p": 0.05, "768p": 0.06, "2k": 0.13, "4k": 0.16}, "extra_charges": {"free_reference_images": 5, "per_reference_image": 0.08}},
    },
}
