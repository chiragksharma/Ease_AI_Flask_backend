from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from applications.tools.commentor import generate_comment

# Create a Blueprint named 'comments'
comments_bp = Blueprint('comments', __name__)
load_dotenv()

@comments_bp.route('/comment', methods=['POST'])
def comment():
    data = request.json
    video_title = data.get('video_title')
    channel_name = data.get('channel_name')
    # Accessing the 'prompt' dictionary from the data
    prompt = data.get('prompt', {})

    # Extracting the 'inputField' value from the 'prompt' dictionary and assigning it to 'tone'
    custom_instruction = prompt.get('inputField')
    tone = prompt.get('selectedButton')

    # for field in input_fields:
    #     if field.get('placeholder') == 'Tone':
    #         tone = field.get('field_value', 'neutral')
    #         break

    try:
        comment = generate_comment(video_title, channel_name, tone,custom_instruction)
        return jsonify({"comment": comment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
