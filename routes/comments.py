from flask import Blueprint, request, jsonify
import requests

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/linkedin', methods=['GET'])
def scrape_comments():
    return jsonify({'comments': 'something', 'sentiments': 'something'})


