# AI Image & Video Studio

fal.ai modellerini kullanarak görsel ve video üretmeye yarayan, FastAPI tabanlı bir web uygulaması. Uygulama; model seçimi, referans görsel yükleme, özel fal.ai endpoint'i kullanma ve tahmini maliyet gösterimi özelliklerini içerir.

## Özellikler

- Görsel düzenleme ve üretim modelleri
- Görselden videoya ve referanstan videoya üretim
- Referans görsel yükleme
- Özel `fal-ai/` endpoint desteği
- Çözünürlük, süre ve en-boy oranı seçenekleri
- Tahmini üretim maliyeti gösterimi
- Üretilen görsel ve videoları indirme

## Gereksinimler

- Python 3.10 veya üzeri
- Bir [fal.ai](https://fal.ai/) API anahtarı

## Kurulum

Depoyu klonlayın ve proje klasörüne geçin:

```bash
git clone https://github.com/azranurtekbas/image_gen_appimage.git
cd image_gen_appimage
```

Sanal ortam oluşturup etkinleştirin:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Bağımlılıkları yükleyin:

```bash
pip install -r backend/requirements.txt
```

Ortam değişkeni dosyasını oluşturun:

```powershell
Copy-Item .env.example .env
```

macOS/Linux için:

```bash
cp .env.example .env
```

Ardından `.env` içindeki değeri kendi anahtarınızla değiştirin:

```env
FAL_KEY=your_fal_api_key_here
```

> `.env` dosyasını veya gerçek API anahtarınızı Git'e eklemeyin. Bu dosya `.gitignore` ile hariç tutulmuştur.

## Çalıştırma

Proje kök dizinindeyken:

```bash
uvicorn main:app --app-dir backend --reload --port 8003
```

Tarayıcıda [http://localhost:8003](http://localhost:8003) adresini açın. API belgeleri [http://localhost:8003/docs](http://localhost:8003/docs) adresindedir.

## Proje yapısı

```text
backend/    FastAPI sunucusu, model kayıtları ve fiyat hesaplamaları
frontend/   HTML, CSS ve JavaScript arayüzü
```

Yüklenen referanslar ve oluşturulan çıktılar çalışma sırasında `uploads`/`outputs` klasörlerine kaydedilir ve Git'e dahil edilmez.

## Güvenlik

- API anahtarları yalnızca yerel `.env` dosyasında tutulmalıdır.
- Uygulamayı internete açmadan önce CORS, kimlik doğrulama, istek sınırlama ve yükleme politikalarını üretim ortamınıza göre sıkılaştırın.
- Daha önce paylaşılan veya commit edilen bir anahtar varsa sağlayıcı panelinden iptal edip yenisini oluşturun.
