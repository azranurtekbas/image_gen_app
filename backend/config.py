"""Uygulama yapılandırması ve ortam değişkenleri."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
load_dotenv(PROJECT_DIR / ".env")

# fal.ai istemcisi, FAL_KEY ortam değişkenini kullanır.
FAL_KEY = os.getenv("FAL_KEY")
