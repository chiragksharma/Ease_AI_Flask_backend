import replicate
from dotenv import load_dotenv
from flask import Flask, request, jsonify,send_file
import os
import requests
import tempfile
from PIL import Image
from io import BytesIO
from api_manager import ReplicateAPIClient

load_dotenv()

def load_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return Image.open(BytesIO(response.content))

def resize_to_fixed_size(image, size=(700, 700)):
    return image.resize(size, Image.Resampling.LANCZOS)

def resize_to_aspect_ratio(image, aspect_ratio=(16, 9)):
    original_width, original_height = image.size
    original_aspect_ratio = original_width / original_height

    if original_aspect_ratio > aspect_ratio[0] / aspect_ratio[1]:
        new_width = original_width
        new_height = int(original_width / (aspect_ratio[0] / aspect_ratio[1]))
    else:
        new_height = original_height
        new_width = int(original_height * (aspect_ratio[0] / aspect_ratio[1]))

    new_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))
    new_image.paste(image, ((new_width - original_width) // 2, (new_height - original_height) // 2))

    return new_image

def create_final_image(image1_url, image2_url):
    # Load images
    image1 = load_image_from_url(image1_url)
    image2 = load_image_from_url(image2_url)

    # Resize the second image to 600x600
    image2_resized = resize_to_fixed_size(image2)

    # Ensure both images are in the same mode
    if image1.mode != 'RGBA':
        image1 = image1.convert('RGBA')
    if image2_resized.mode != 'RGBA':
        image2_resized = image2_resized.convert('RGBA')

    # Calculate offset to place the second image at the bottom right corner
    offset = (image1.width - image2_resized.width, image1.height - image2_resized.height)

    # Create a new image with a white background the size of the first image
    new_image = Image.new('RGBA', (image1.width, image1.height), (255, 255, 255, 255))
    new_image.paste(image1, (0, 0))

    # Paste the second image into the new image at the calculated offset
    new_image.paste(image2_resized, offset, image2_resized)

    return new_image.convert('RGB')


def generate_image(video_title, channel_name, channel_logo, user_image, pose):
    # prompt1 = "A shocking face closeup for youtube thumnail, fingers pointing to the left"
    # prompt2 = "image of a yellow Lamborghini Aventador parked on a vibrant green grassy field under a bright blue sky with some clouds. The car is positioned prominently, and there's an arrow pointing to it with the text 'EDIT ME!' above."
    # image_url = "https://replicate.delivery/pbxt/KIIutO7jIleskKaWebhvurgBUlHR6M6KN7KHaMMWSt4OnVrF/musk_resize.jpeg"
    # pose_image_url = "https://replicate.delivery/pbxt/KJmFdQRQVDXGDVdVXftLvFrrvgOPXXRXbzIVEyExPYYOFPyF/80048a6e6586759dbcb529e74a9042ca.jpeg"
    # test_background_image = "https://i.pinimg.com/564x/e4/a4/5c/e4a45cb6f4902f67710f69e57f38b847.jpg"
    prompt1 = f"""
    Create an AI-generated image of a person based on the video titled '{video_title}'. 
    The image should prominently feature a close-up of the user's face with a highly expressive reaction that matches the emotion conveyed by the video's title. 
    Use the provided user image as a reference for the person's appearance. 
    Ensure that the facial expression is the focal point. 
    The expression should clearly convey the primary emotion suggested by the video title (e.g., excitement, surprise, fear, joy). 
    Ensure the generated image is visually appealing, highly detailed, and accurately represents the person based on the reference image.
    """  
    prompt2 =f"""
    Create a visually appealing YouTube thumbnail background for a video titled '{video_title}'. 
    You are a proffesional senior graphic designer and creates visually appealing thumbnails that actually have high click rate.
    The background should be vibrant and eye-catching, incorporating elements that reflect the video's theme. 
    Include a small piece of text that is SEO optimized and best suited for the thumbnail based on the video title. 
    Note: This text should be positioned in the top left corner only and be highly engaging. 
    Also keep in mind the that text should not be more than three four words. It should be in the top left corner of the image only.
    Ensure the background and text combination grabs attention instantly and complements the overall theme and emotion of the video.
    """
    try:
        generated_image_urls = ReplicateAPIClient.generate_image_from_pose(user_image, prompt1, pose)
        if not generated_image_urls or not isinstance(generated_image_urls, list):
            raise ValueError("Invalid response for generated image URLs")

        generated_image_url = generated_image_urls[0]
        print("Generated image url",generated_image_url)
        image_with_removed_bg_url = ReplicateAPIClient.remove_background_image(generated_image_url)
        print("Removed Bg image url",image_with_removed_bg_url)
        text_generated_image_urls = ReplicateAPIClient.generate_image_with_text(prompt2)
        text_generated_image_url=text_generated_image_urls[0]
        print("text generated image url",text_generated_image_url)
        final_image = create_final_image(text_generated_image_url, image_with_removed_bg_url)
        print("generated final image",final_image)
    except Exception as e:
        return f"Error generating image: {e}"

    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        final_image.save(temp_file.name)
    except Exception as e:
        return f"Error saving final image: {e}"

    return send_file(temp_file.name, mimetype='image/jpeg')