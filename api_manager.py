# api_manager.py
import os
from openai import OpenAI
import replicate
import requests

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

class ReplicateAPIClient:
    _client=None
    
    replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
    @classmethod
    def generate_image_from_pose(cls,image_url,prompt,pose_image_url):
        model = replicate.models.get("zsxkib/instant-id")
        input = {
        "image": image_url,
        "prompt": prompt,
        "pose_image": pose_image_url,
        "sdxl_weights": "protovision-xl-high-fidel",
        "guidance_scale": 5,
        "negative_prompt": "(lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured (lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch,deformed, mutated, cross-eyed, ugly, disfigured"
        }

        output = replicate.run(
            "zsxkib/instant-id:f1ca369da43885a347690a98f6b710afbf5f167cb9bf13bd5af512ba4a9f7b63",
            input=input
        )

        return output
    
    @classmethod
    def generate_image_with_text(cls,prompt):
        input = {
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "output_quality": 79,
            "negative_prompt": "ugly, distorted"
        }

        output = replicate.run(
            "stability-ai/stable-diffusion-3",
            input=input
        )

        return output

    @classmethod
    def remove_background_image(cls,image_url):
        input = {
            "image": image_url
        }
        output = replicate.run(
            "cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
            input=input
        )
        return output

    



