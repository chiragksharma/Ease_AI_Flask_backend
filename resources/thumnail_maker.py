from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from applications.tools.ai_thumbnail import generate_image

# Create a Blueprint named 'comments'
ai_thumbnail = Blueprint('thumnail', __name__)
load_dotenv()

@ai_thumbnail.route('/thumbnail', methods=['POST'])
def ai_image():
    try:
        data = request.get_json()
        video_title = data.get('video_title')
        channel_name = data.get('channel_name')
        channel_logo = data.get('channel_logo')
        user_image = data.get('user_image')
        pose = data.get('pose')

        image = generate_image(video_title, channel_name, channel_logo, user_image, pose)
        
        return image
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500
