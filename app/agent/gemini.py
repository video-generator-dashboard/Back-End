import os
import logging
from typing import Any, Dict, Optional
from fastapi.concurrency import run_in_threadpool

import asyncio

from .base import BaseProvider

try:
    from google import genai
except ImportError:
    raise ImportError("Please install google-genai: pip install google-genai")

from google.genai import types
try:
    from PIL import Image
except ImportError:
    raise ImportError("Please install pillow: pip install pillow")
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("Gemini API key is missing")
        self.model = model
        self._client = genai.Client(api_key=api_key)

    def _generate_sync(self, prompt: str, options: Dict[str, Any]) -> str:
        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response.text is not None else "[Boş cevap döndü]"
        except Exception as e:
            raise Exception(f"Gemini - error generating response: {e}") from e

    async def __call__(self, prompt: str, **generation_args: Any) -> str:
        opts = {}
        return await run_in_threadpool(self._generate_sync, prompt, opts)

    async def generate_video_script(self, title: str, time: int, **generation_args) -> str:
        prompt = f"""{time} saniyelik "{title}" konulu bir video senaryosu oluştur.
Video senaryosunu sahneler halinde zamanlara böl. Her bir sahne için başlangıç ve bitiş zamanı, sahneye uygun detaylı bir resim açıklaması ve varsa ekranda belirecek metin (text overlay) belirt.

Videoda baştan sona konseptle uyumlu, telifsiz sabit bir fon müziği çalacak.

Yanıtını SADECE aşağıdaki JSON formatında ver ama başında veya sonunda json yazmasın bir api gibi döndür:

{{
    "video_title": "{title} Videosu",
    "background_music": "Telifsiz Müzik Adı (Örn: 'Happy Acoustic Folk')",
    "scenes": [
        {{
            "start_time": "0:00",
            "end_time": "0:10",
            "image_description": "güneş aymış ve güzelce uyanan bir küçük kız şirin bir evde",
            "text_overlay": "Güne iyi başla"
        }},
        {{
            "start_time": "0:10",
            "end_time": "0:20",
            "image_description": "güzel bir doğa yürüyüşü kuşlar ve çiçekler",
            "text_overlay": null
        }}
    ]
}}
"""
        return await self.__call__(prompt, **generation_args)

"""
async def main():
    title = "derslerin önemini anlatan bir video"
    time = 5
    provider = GeminiProvider(model="gemini-2.0-flash", api_key="AIzaSyDvocvIc1gg3gP3gVlH5hbSKWUEGivrxIw")
    response = await provider.generate_video_script(title, time, temperature=0.7, top_p=0.95, max_length=256)
    print(f"Cevap:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())
"""

class ImageProcessor:
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-preview-image-generation"):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("Gemini API key is missing")
        self.model = model
        self._client = genai.Client(api_key=api_key)

    async def generate_image(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._generate_image_sync, prompt)

    def _generate_image_sync(self, prompt: str) -> str:
        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                )
            )
            candidates = getattr(response, "candidates", None)
            if not candidates or len(candidates) == 0:
                return "[Görsel veya metin bulunamadı]"
            content = getattr(candidates[0], "content", None)
            if not content or not hasattr(content, "parts"):
                return "[Görsel veya metin bulunamadı]"
            # Önce image varsa onu döndür
            for part in content.parts:
                inline_data = getattr(part, "inline_data", None)
                if inline_data and getattr(inline_data, "data", None):
                    image_bytes = inline_data.data
                    if isinstance(image_bytes, bytes):
                        return base64.b64encode(image_bytes).decode("utf-8")
            # Sonra varsa metni döndür
            for part in content.parts:
                text = getattr(part, "text", None)
                if isinstance(text, str):
                    return text
            return "[Görsel veya metin bulunamadı]"
        except Exception as e:
            raise Exception(f"Gemini Image - error generating image: {e}") from e

"""
if __name__ == "__main__":
    import os
    async def main():
        processor = ImageProcessor()  # .env'den otomatik API key alır
        prompt = "3 boyutlu, kanatlı ve şapkalı bir domuzun, mutlu ve yeşil bir bilimkurgu şehrinin üzerinde uçtuğu bir sahne"
        base64_image = await processor.generate_image(prompt)
        print("Base64 Görsel (ilk 100 karakter):", base64_image[:100] + "...")

        # Görseli public/images klasörüne kaydet
        images_dir = os.path.join(os.path.dirname(__file__), '../../public/images')
        os.makedirs(images_dir, exist_ok=True)
        image_path = os.path.join(images_dir, 'output.png')
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))
        image.save(image_path)
        print(f"Görsel kaydedildi: {image_path}")
    import asyncio
    asyncio.run(main())
"""