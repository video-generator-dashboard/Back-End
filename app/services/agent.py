from functools import lru_cache
import functools
from typing import Optional
from unittest import result
from app.agent.gemini import GeminiProvider, ImageProcessor
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
import json

load_dotenv()

class AgentService:
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash", title="herhangi bir konu", time=10):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise Exception("GEMINI_API_KEY is not set in .env or as a parameter.")
        self.provider = GeminiProvider(api_key=api_key, model=model)
        self.image_processor = ImageProcessor(api_key=api_key)
        self.images = []
        self.json_video_response = ""
        self.title = title
        self.time = time

    async def generate_video_script(self, title: str, time: int, **generation_args) -> str:
        return await self.provider.generate_video_script(title, time, **generation_args)

    def clean_json_response(self, json_string: str) -> str:
        """
        JSON string'ini temizler.
        Başındaki ve sonundaki boşlukları kaldırır.
        ```json, ``` gibi markdown işaretlerini kaldırır.
        "json" ile başlayan satırları temizler.
        Sadece saf JSON string'ini döndürür.
        """
        json_string = json_string.strip()
        json_string = json_string.replace("```json", "").replace("```", "")

        lines = json_string.splitlines()
        cleaned_lines = []
        for line in lines:
            if not line.strip().lower().startswith("json"):
                cleaned_lines.append(line)
        json_string = "\n".join(cleaned_lines)

        return json_string
    

    @lru_cache(maxsize=256)
    async def generate_video_base(self):
        json_result = await self.generate_video_script(self.title, self.time, temperature=0.7, top_p=0.95, max_length=256)
        self.json_video_response = self.clean_json_response(json_result).strip()


    @lru_cache(maxsize=256)
    async def generate_images(self):
        try:
            # JSON'ı parse et
            video_data = json.loads(self.json_video_response)
            
            # Video klasörünü oluştur
            dir = self.title.replace(" ", "_")
            dir = dir.lower()
            list_dir = dir.translate(str.maketrans('çğışöü', 'cgisuo'))
            video_dir = os.path.join(os.path.dirname(__file__), f'../public/{list_dir}')
            images_dir = os.path.join(video_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            # self.images listesini temizle
            self.images = []
            
            # Her sahne için görsel üret
            scenes = video_data.get('scenes', [])
            for i, scene in enumerate(scenes):
                image_description = scene.get('image_description', '')
                if image_description:
                    print(f"Görsel {i+1} üretiliyor: {image_description[:50]}...")
                    
                    # Görsel üret
                    base64_image = await self.image_processor.generate_image(image_description)
                    
                    # Görseli kaydet
                    image_filename = f"{i+1:03d}.jpeg"  # 001, 002, 003 formatında
                    image_path = os.path.join(images_dir, image_filename)
                    
                    image_data = base64.b64decode(base64_image)
                    image = Image.open(BytesIO(image_data))
                    image.save(image_path, 'JPEG')
                    
                    # Görsel yolunu listeye ekle
                    relative_path = f"public/{self.title}/images/{image_filename}"
                    self.images.append(relative_path)
                    
                    print(f"Görsel kaydedildi: {image_path}")
            
            print(f"Toplam {len(self.images)} adet görsel üretildi.")
            
        except json.JSONDecodeError as e:
            print(f"JSON parse hatası: {e}")
            self.images = []
        except Exception as e:
            print(f"Görsel üretme hatası: {e}")
            self.images = []


if __name__ == "__main__":
    async def main():

        title = "derslerin önemini anlatan bir video"
        time = 5
        agent = AgentService(title=title, time=time)
        await agent.generate_video_base()
        await agent.generate_images()
       
    
    import asyncio
    asyncio.run(main()) 