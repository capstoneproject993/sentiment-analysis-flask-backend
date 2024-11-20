from flask import Flask
from flask_cors import CORS
from routes.comments import comments_bp
from model import *



app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(comments_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
