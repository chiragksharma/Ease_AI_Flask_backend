from flask import Flask
from resources.comment import comments_bp  # Import the Blueprint
from resources.thumnail_maker import ai_thumbnail
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.register_blueprint(comments_bp)  # You can specify a prefix if needed
app.register_blueprint(ai_thumbnail)

if __name__ == "__main__":
    app.run(debug=True)