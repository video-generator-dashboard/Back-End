from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv 

import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base() #sqlalchemy için bu sınıfı kullanıyoruz 'class DBUser(Base)' şeklinde tanımlıyoruz
class Base(DeclarativeBase):
    pass #yeni sqlalchemy sürümünde bu sınıfı kullanıyoruz

def init_db():
    Base.metadata.drop_all(engine)   # Veritabanını her başlangıcta siler burayada dikkat !!!!!!!!
    Base.metadata.create_all(bind=engine) # Veritabanını oluşturur

# Session dependency (FastAPI için)
def get_session_db():
    db = SessionLocal()
    try:
        yield db #donen değer yield olduğuna dikkat
    finally:
        db.close() 


