import requests
from flask import current_app


class AIServiceError(Exception):
    pass


class AIService:
    def _system_mesaji(self):
        return current_app.config["BUSINESS_CONTEXT"]

    def yanit_uret(self, mesaj, gecmis=None):
        api_key = current_app.config.get("GROQ_API_KEY")

        if not api_key:
            return "Demo modu aktif. Groq API anahtarı bulunamadı."

        messages = [
            {
                "role": "system",
                "content": self._system_mesaji()
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": messages,
                    "temperature": 0.7
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as hata:
            raise AIServiceError(
                "Yapay zeka servisine baglanirken bir hata olustu."
            ) from hata


ai_service = AIService()