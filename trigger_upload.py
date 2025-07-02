# trigger_upload.py
import requests
import json
import os

# FastAPI uygulamanızın çalıştığı adres
FASTAPI_URL = "http://127.0.0.1:8000/api/generate_and_upload_video"

# JSON veri dosyasının yolu
JSON_FILE_PATH = "content.json"

# İşlenmiş videoların kaydedileceği dosya
PROCESSED_VIDEOS_FILE = "processed_videos.txt"

headers = {"Content-Type": "application/json"}

def load_video_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_processed_videos(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_video(file_path, video_title):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(video_title + '\n')

if __name__ == "__main__":
    try:
        video_data_list = load_video_data(JSON_FILE_PATH)
        processed_videos = load_processed_videos(PROCESSED_VIDEOS_FILE)
        
        for i, video_data in enumerate(video_data_list):
            # YouTube başlığına benzersiz bir kimlik ekle
            # Bu, her çalıştırmada benzersiz bir başlık oluşturur
            current_youtube_title = f"{video_data["youtube_title"]} - {os.urandom(4).hex()}"
            
            if current_youtube_title in processed_videos:
                print(f"Video {i+1}: '{current_youtube_title}' zaten işlenmiş, atlanıyor.")
                continue

            print(f"\nProcessing video {i+1}/{len(video_data_list)}: '{current_youtube_title}'...")
            
            # API'ye gönderilecek payload'ı hazırla
            payload = video_data.copy()
            payload["youtube_title"] = current_youtube_title

            try:
                response = requests.post(FASTAPI_URL, data=json.dumps(payload), headers=headers)
                response.raise_for_status() # HTTP hataları için istisna fırlatır
                
                response_json = response.json()
                print("Video oluşturma ve yükleme isteği başarıyla gönderildi.")
                print(response_json)
                
                if response_json.get("status") == "success":
                    save_processed_video(PROCESSED_VIDEOS_FILE, current_youtube_title)
                    print(f"Video '{current_youtube_title}' başarıyla işlendi ve kaydedildi.")

            except requests.exceptions.RequestException as e:
                print(f"İstek gönderilirken bir hata oluştu: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Yanıt içeriği: {e.response.text}")

    except FileNotFoundError:
        print(f"Hata: {JSON_FILE_PATH} dosyası bulunamadı.")
    except json.JSONDecodeError:
        print(f"Hata: {JSON_FILE_PATH} dosyası geçersiz bir JSON formatına sahip.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")