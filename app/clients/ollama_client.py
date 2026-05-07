import requests
from typing import Any, List, Dict, Optional
from app.clients.base import BaseModelClient
from app.core.settings import settings

class OllamaClient(BaseModelClient):
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"

    def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        **kwargs: Any
    ) -> str:

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": kwargs.get("options", {})
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.generate_url, json=payload, timeout=kwargs.get("timeout", 30))
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Ollama Generate Error: {e}")
            return f"Error: Could not connect to Ollama for model {model}."

    def chat(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        **kwargs: Any
    ) -> str:

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": kwargs.get("options", {})
        }

        try:
            response = requests.post(self.chat_url, json=payload, timeout=kwargs.get("timeout", 60))
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Ollama Chat Error: {e}")
            return f"Error: Chat failed for model {model}."

ollama_client = OllamaClient()