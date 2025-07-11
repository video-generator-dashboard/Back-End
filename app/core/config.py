#from passlib.context import CryptContext
import os
from fastapi.middleware.cors import CORSMiddleware # Bu importu ekle
from ..main import app
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
"""

# CORS Ayarları
# Ön yüzünüzün çalıştığı URL'i buraya ekleyin
origins = [
    "http://localhost:3000", # React uygulamanızın çalıştığı adres
    # "https://your-frontend-domain.com", # Canlı ortamda frontend domain'iniz
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Kimlik doğrulama çerezlerinin gönderilmesine izin ver
    allow_methods=["*"],    # Tüm HTTP metotlarına izin ver (GET, POST, PUT, DELETE vb.)
    allow_headers=["*"],    # Tüm başlıklara izin ver
)





