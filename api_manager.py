# api_manager.py
import os
from openai import OpenAI

class APIClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("API Key for OpenAI is not set in the environment variables")
            cls._client = OpenAI(api_key=api_key)
        return cls._client

    @classmethod
    def generate_chat_completion(cls, prompt, model="gpt-3.5-turbo"):
        client = cls.get_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model
        )
        response = chat_completion.choices[0].message.content
        return response
