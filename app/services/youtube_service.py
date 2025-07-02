import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API kapsamları
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Jeton dosyası (kimlik doğrulama sonrası oluşturulacak)
TOKEN_FILE = "token.pickle"

def get_authenticated_service():
    creds = None
    # Jeton dosyası varsa, kimlik bilgilerini yükle
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Kimlik bilgileri yoksa veya geçersizse, kimlik doğrulama akışını başlat
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Get client ID and client secret from environment variables
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

            if not client_id or not client_secret:
                raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env file")

            client_config = {
                "web": {
                    "client_id": client_id,
                    "project_id": "your-project-id", # This can be a placeholder or read from .env if needed
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": ["http://localhost"]
                }
            }
            flow = InstalledAppFlow.from_client_config(
                client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        # Kimlik bilgilerini kaydet
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

async def upload_video_to_youtube(video_filepath: str, title: str, description: str, tags: list, privacy_status: str):
    youtube = get_authenticated_service()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '28' # Category for Science & Technology
        },
        'status': {
            'privacyStatus': privacy_status # Can be 'public', 'private', or 'unlisted'
        }
    }

    media_body = MediaFileUpload(video_filepath, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media_body
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if response is not None:
            if 'id' in response:
                print(f"Video id {response['id']} was successfully uploaded.")
                return f"https://www.youtube.com/watch?v={response['id']}"
            else:
                print(f"The upload failed with an unexpected response: {response}")
                return None