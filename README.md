# YouTube Shorts Generator

Bu proje, metin girdisinden otomatik olarak YouTube Shorts videoları oluşturan bir FastAPI uygulamasıdır. Metin işleme, metinden sese dönüştürme, görsel oluşturma ve video birleştirme gibi adımları içerir.

## Özellikler (MVP)

- Metni cümlelere ayırma
- Her cümle için ses dosyası oluşturma (gTTS kullanarak)
- Her cümle için metin içeren görsel kareler oluşturma (Pillow kullanarak)
  - Metinler, yarı saydam beyaz bir arka plan kutusu üzerinde siyah renkte görünür.
- Ses ve görsel kareleri birleştirerek nihai video oluşturma (MoviePy kullanarak)
- **Video Şablonu Desteği:** İsteğe bağlı olarak, arka plan olarak kullanılacak bir video şablonu seçilebilir.
- **Arka Plan Müziği Desteği:** İsteğe bağlı olarak, videoya arka plan müziği eklenebilir. Konuşma sesi ile müziğin seviyeleri ayarlanabilir.
- Üretilen videolar `static/temp/videos/` dizininde kalıcı olarak saklanır.
- **YouTube Otomatik Yükleme:** Üretilen videoları doğrudan YouTube'a yükleme yeteneği.
- **API Üzerinden Otomatik Video Oluşturma ve Yükleme:** JSON payload ile programatik olarak video oluşturma ve YouTube'a yükleme.
- Basit web arayüzü ile metin girişi ve video çıktısı görüntüleme

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

### 1. Projeyi Klonlayın

```bash
git clone <proje_deposu_url>
cd youtube_shorts_generator
```

### 2. Python Sanal Ortamı Oluşturun ve Etkinleştirin

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. FFmpeg Kurulumu

`moviepy` kütüphanesi videoları işlemek için sisteminizde `ffmpeg`'in kurulu olmasını gerektirir. Eğer kurulu değilse, `moviepy` video oluştururken hata verecektir. İşletim sisteminize göre aşağıdaki komutlardan birini kullanarak `ffmpeg`'i yükleyebilirsiniz:

- **macOS (Homebrew ile):**
  ```bash
  brew install ffmpeg
  ```
- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **Windows:** `ffmpeg`'i [resmi web sitesinden](https://ffmpeg.org/download.html) indirip PATH'inize eklemeniz gerekmektedir.

### 5. Font Dosyası Ekleme

Metin görselleri için bir font dosyasına ihtiyacınız var. `static/fonts/` dizini altına `Montserrat.ttf` adında bir font dosyası yerleştirin. Eğer farklı bir font kullanmak isterseniz, `app/config.py` dosyasındaki `FONT_PATH` değişkenini güncelleyebilirsiniz.

```bash
mkdir -p static/fonts
# Montserrat.ttf dosyasını buraya kopyalayın
```

### 6. Video Şablonu Ekleme (İsteğe Bağlı)

Arka plan olarak kullanmak istediğiniz video şablonlarını `static/templates/` dizini altına yerleştirin. Desteklenen formatlar `.mp4`, `.mov`, `.avi` vb. olabilir.

```bash
mkdir -p static/templates
# template.mp4 dosyasını buraya kopyalayın
```

### 7. Arka Plan Müziği Ekleme (İsteğe Bağlı)

Videoya eklemek istediğiniz arka plan müzik dosyalarını `static/music/` dizini altına yerleştirin. Desteklenen formatlar `.mp3`, `.wav` vb. olabilir.

```bash
mkdir -p static/music
# background_music.mp3 dosyasını buraya kopyalayın
```

### 8. YouTube API Kimlik Bilgileri

YouTube'a video yüklemek için Google Cloud projenizden OAuth 2.0 kimlik bilgilerine ihtiyacınız var. Bu bilgileri doğrudan Git deposuna yüklemeyin. Bunun yerine, projenizin kök dizinindeki `.env` dosyasına aşağıdaki gibi ekleyin:

```
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET
```

- **`YOUR_CLIENT_ID`** ve **`YOUR_CLIENT_SECRET`** yerine kendi Google Cloud Console'dan aldığınız değerleri yapıştırın.
- İlk yükleme denemenizde bir tarayıcı penceresi açılacak ve Google hesabınızla kimlik doğrulama yapmanız istenecektir. Kimlik doğrulama başarılı olduğunda, erişim jetonları `token.pickle` dosyasına kaydedilecektir. Bu dosyayı da `.gitignore`'a eklemeyi unutmayın.

## Kullanım

### Web Arayüzü Üzerinden

Uygulamayı başlatmak için sanal ortamınız etkinleştirilmişken aşağıdaki komutu çalıştırın:

```bash
uvicorn app.main:app --reload
```

Uygulama `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır. Web tarayıcınızdan bu adresi ziyaret ederek metin girip video oluşturabilirsiniz. Şablon videoları ve müzik dosyaları eklediyseniz, ilgili açılır listelerden seçim yapabilirsiniz. Video oluşturulduktan sonra YouTube'a yükleme seçenekleri sunulacaktır.

### API Endpoint Üzerinden (Otomatik Yükleme İçin)

Uygulama, JSON payload ile otomatik video oluşturma ve YouTube'a yükleme için bir API endpoint'i sunar.

- **URL:** `http://127.0.0.1:8000/api/generate_and_upload_video`
- **HTTP Yöntemi:** `POST`
- **İçerik Tipi (Content-Type):** `application/json`

**JSON Yükü Yapısı:**

```json
{
    "text": "string",
    "music_name": "string (optional)",
    "template_name": "string (optional)",
    "youtube_title": "string",
    "youtube_description": "string (optional)",
    "youtube_tags": ["string", "string", "..."] (optional),
    "youtube_privacy_status": "string" (public, private, unlisted)
}
```

**Örnek `curl` Komutu:**

```bash
curl -X POST "http://127.0.0.1:8000/api/generate_and_upload_video" \
-H "Content-Type: application/json" \
-d '{
    "text": "Bu bir API testi videosudur. Otomatik olarak oluşturuldu ve yüklendi.",
    "music_name": "your_music_file.mp3",
    "template_name": "your_template_video.mp4",
    "youtube_title": "API Test Videosu - Yeni Deneme",
    "youtube_description": "Bu video API endpoint üzerinden gönderilen JSON verisi ile oluşturulmuştur.",
    "youtube_tags": ["api", "test", "fastapi", "youtube"],
    "youtube_privacy_status": "unlisted"
}'
```

### Otomatik Çalıştırma (Cron Job Örneği)

`content.json` dosyasındaki verileri kullanarak videoları otomatik olarak oluşturmak ve yüklemek için `trigger_upload.py` betiğini kullanabilirsiniz. Bu betik, her çalıştığında `content.json`'daki işlenmemiş videoları bulur ve yükler. İşlenen videolar `processed_videos.txt` dosyasına kaydedilir.

**`trigger_upload.py`'yi Çalıştırma:**

```bash
./venv/bin/python trigger_upload.py
```

Bu betiği belirli aralıklarla çalıştırmak için Cron (Linux/macOS) veya Görev Zamanlayıcı (Windows) gibi harici bir zamanlayıcı kullanabilirsiniz.

**Cron Job Örneği (her saat başı çalıştırmak için):**

```cron
0 * * * * /bin/bash -c "source venv/bin/activate && python trigger_upload.py >> cron.log 2>&1"
```

## Proje Yapısı

```
. 
├── app/
│   ├── main.py                    # FastAPI ana uygulama
│   ├── models/
│   │   └── video_models.py        # Pydantic request/response modelleri
│   ├── services/
│   │   ├── __init__.py
│   │   ├── text_processor.py      # Metin işleme ve cümle ayırma
│   │   ├── tts_service.py         # gTTS ile ses üretimi
│   │   ├── image_service.py       # PIL ile görsel oluşturma
│   │   ├── video_service.py       # MoviePy ile video birleştirme
│   │   └── youtube_service.py     # YouTube API entegrasyonu
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_manager.py        # Dosya yönetimi utilities
│   └── config.py                  # Konfigürasyon ayarları
├── static/
│   ├── css/
│   │   └── style.css             # Basit CSS stilleri
│   ├── js/
│   │   └── main.js               # Frontend JavaScript
│   ├── fonts/                    # Font dosyaları
│   │   └── Montserrat.ttf
│   ├── templates/                # Video şablonları
│   │   └── your_template.mp4
│   ├── music/                    # Arka plan müzikleri
│   │   └── your_music.mp3
│   └── temp/                     # Geçici dosyalar (otomatik temizlenmez)
│       ├── audio/
│       ├── images/
│       └── videos/
├── templates/
│   ├── base.html                 # Ana template
│   ├── index.html                # Ana form sayfası
│   ├── result.html               # Sonuç sayfası
│   ├── youtube_upload_success.html # YouTube yükleme başarı sayfası
│   ├── youtube_upload_failure.html # YouTube yükleme hata sayfası
│   ├── header.html               # Header parçası
│   └── footer.html               # Footer parçası
├── requirements.txt              # Python bağımlılıkları
├── .env                         # Ortam değişkenleri (hassas bilgiler)
├── .gitignore                   # Git tarafından göz ardı edilecek dosyalar
├── README.md                    # Proje dokümantasyonu
├── content.json                 # Otomatik yükleme için JSON veri dosyası
├── trigger_upload.py            # Otomatik yükleme betiği
└── processed_videos.txt         # İşlenmiş videoların kaydı
```

## Gelecek Geliştirmeler

- Daha gelişmiş metin işleme ve doğal dil anlama (NLP)
- Farklı video şablonları ve özelleştirme seçenekleri
- Video düzenleme ve kırpma özellikleri
- Farklı seslendirme seçenekleri (erkek/kadın, farklı diller/aksiyonlar)
- Video efektleri ve geçişler
