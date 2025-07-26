import asyncio
from concurrent.futures import ThreadPoolExecutor
from csv import Error
from pyexpat import model
from .base import BaseProvider
from typing import Any, Dict, List, Optional
import ollama
from fastapi.concurrency import run_in_threadpool

class OllamaProvider(BaseProvider):

    def __init__(self, model_name: str = "phi3:mini", host: Optional[str] = None):
        self.model = model_name
        self._client = ollama.Client(host=host) if host else ollama.Client()


    @staticmethod
    async def get_installed_models(host: Optional[str] = None) -> List[str]:
        """
        List all installed models.
        """

        def _list_sync() -> List[str]:
            client = ollama.Client(host=host) if host else ollama.Client()
            return [model_class.model for model_class in client.list().models]

        return await run_in_threadpool(_list_sync)

    def _generate_sync(self, prompt: str, options: Dict[str, Any]) -> str:
        """
        Generate a response from the model.
        """
        try:
            response = self._client.generate(
                prompt=prompt,
                model=self.model,
                options=options,
            )
            return response["response"].strip()
        except Exception as e:
            raise Error(f"Ollama - Error generating response: {e}")

    async def __call__(self, prompt: str, **generation_args: Any) -> str:
        opts = {
            "temperature": generation_args.get("temperature", 0),
            "top_p": generation_args.get("top_p", 0.9),
            "top_k": generation_args.get("top_k", 40),
            "num_ctx": generation_args.get("max_length", 20000),
        }
        return await run_in_threadpool(self._generate_sync, prompt, opts)

async def main():

    ollama_provider = OllamaProvider(model_name="all-minilm:latest")

    print("\n--- Yüklü Ollama Modelleri ---")
    installed_models = await OllamaProvider.get_installed_models()
    if installed_models:
        for model in installed_models:
            print(f"- {model}")
    else:
        print("Yüklü model bulunamadı veya Ollama sunucusuna bağlanılamadı.")

    prompt1 = """10 saniyelik bir senaryo yaz"""
    response1 = await ollama_provider(prompt1, tempature=0.7, top_p=0.9, top_k=50, max_length=100)
    print(f"cevap ---\n{response1}")


_thread_pool_executor = ThreadPoolExecutor(max_workers=5) # İhtiyaca göre worker sayısını ayarlayın

if __name__ == "__main__":
    asyncio.run(main())
    # ThreadPoolExecutor'ı kapatmak için:
    _thread_pool_executor.shutdown(wait=True)