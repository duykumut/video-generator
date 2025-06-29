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

## Kullanım

Uygulamayı başlatmak için sanal ortamınız etkinleştirilmişken aşağıdaki komutu çalıştırın:

```bash
uvicorn app.main:app --reload
```

Uygulama `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır. Web tarayıcınızdan bu adresi ziyaret ederek metin girip video oluşturabilirsiniz. Şablon videoları ve müzik dosyaları eklediyseniz, ilgili açılır listelerden seçim yapabilirsiniz.

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
│   │   └── video_service.py       # MoviePy ile video birleştirme
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
│   ├── header.html               # Header parçası
│   └── footer.html               # Footer parçası
├── requirements.txt              # Python bağımlılıkları
├── .env                         # Environment variables
├── .gitignore
└── README.md
```

## Gelecek Geliştirmeler

- Daha gelişmiş metin işleme ve doğal dil anlama (NLP)
- Farklı video şablonları ve özelleştirme seçenekleri
- Video düzenleme ve kırpma özellikleri
- Asenkron video işleme için kuyruk sistemi (örn. Celery, RabbitMQ)
- Kullanıcı kimlik doğrulama ve video geçmişi