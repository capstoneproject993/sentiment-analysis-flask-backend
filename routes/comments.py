# from .services.linkedincomments import get_linkedin_comments, init_linkedin_scrapper

#linkedin_scrapper = init_linkedin_scrapper()
#@comments_bp.route('/linkedin', methods=['GET'])
#def scrape_comments_linkedin():
#    post_url = request.args.get('url') 
#   comments = get_linkedin_comments(url=post_url, driver=linkedin_scrapper)
#   return jsonify({ 
#       'status':200,
#       'comments': comments,
#        'count': len(comments)
#        })



# 20/11/24
#############################################################
from flask import Blueprint, request, jsonify
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs
import pickle
import numpy as np
from model import TextPreprocessor

# Load the sentiment analysis model
with open("model_naive2.pkl", "rb") as file:
    loaded_model = pickle.load(file)
print("Sentiment analysis model loaded successfully!")

comments_bp = Blueprint('comments', __name__)
@comments_bp.route('/youtube', methods=['GET'])
def scrape_comments_youtube():
    # Get YouTube video URL from the request
    post_url = request.args.get('url')
    if not post_url:
        return jsonify({'status': 400, 'error': 'Missing YouTube video URL'}), 400

    # Parse the video ID from the URL
    parsed_url = urlparse(post_url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v', [None])[0]

    if not video_id:
        return jsonify({'status': 400, 'error': 'Invalid YouTube video URL'}), 400

    # Initialize YouTube API client
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDG9-yoU5uIm7KUa1458wGgyHKz2V0FiUE"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Fetch comments from the YouTube video
    req = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = req.execute()
    comments = []
    for item in response["items"]:
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment_text)

    # Predict sentiments for the comments
    if not comments:
        return jsonify({'status': 200, 'message': 'No comments found', 'comments': []}), 200

    predictions = loaded_model.predict(comments)

    # Count the number of 1s, 0s, and -1s in the predictions
    positive_count = np.sum(predictions == 1)
    neutral_count = np.sum(predictions == 0)
    negative_count = np.sum(predictions == -1)

    print("Scraped Comments:", comments)
    print("Predicted Sentiments:", predictions)
    print("Sentiment Counts:", {
        'positive': int(positive_count),
        'neutral': int(neutral_count),
        'negative': int(negative_count)
    })

    return jsonify({
        'status': 200,
        'comments': comments,
        'sentiments': predictions.tolist(),
        'sentiment_counts': {
            'positive': int(positive_count),
            'neutral': int(neutral_count),
            'negative': int(negative_count)
        }
    })
