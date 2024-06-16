import os
from dotenv import load_dotenv
from flask import request, jsonify
from openai import OpenAI
from api_manager import APIClient

load_dotenv()

def generate_comment(video_title, channelName, tone,custom_instruction):

    prompt = f"Generate a  comment for a YouTube video with the title '{video_title}' and the channel Name: '{channelName}' in this tone '{tone}'.Follow these instructions while generating the prompt:'{custom_instruction}'. " \
             f"The comment should sound realistic and not ai generated.word limit 10 words and no hashtags"
    response = APIClient.generate_chat_completion(prompt)
    return response

