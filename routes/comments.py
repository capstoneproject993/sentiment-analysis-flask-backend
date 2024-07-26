from flask import Blueprint,request, jsonify
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import urlparse, parse_qs
from .services.linkedincomments import get_linkedin_comments, init_linkedin_scrapper

comments_bp = Blueprint('comments', __name__)

linkedin_scrapper = init_linkedin_scrapper()
@comments_bp.route('/linkedin', methods=['GET'])
def scrape_comments_linkedin():
    post_url = request.args.get('url') 
    comments = get_linkedin_comments(url=post_url, driver=linkedin_scrapper)
    return jsonify({ 
        'status':200,
        'comments': comments,
        'count': len(comments)
        })


@comments_bp.route('/youtube', methods=['GET'])
def scrape_comments_youtube():
    post_url = request.args.get('url')
    print(post_url)
    parsed_url = urlparse(post_url)
    query_params = parse_qs(parsed_url.query)
    
    video_id = query_params.get('v', [None])[0]
    print(video_id)
    api_service_name="youtube"
    api_version="v3"
    DEVELOPER_KEY="AIzaSyDG9-yoU5uIm7KUa1458wGgyHKz2V0FiUE"

    youtube= googleapiclient.discovery.build(api_service_name,
        api_version,developerKey=DEVELOPER_KEY)
    req = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    response=req.execute()
    comments=[]
    for item in response["items"]:
        name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment = { 'user':name, 'comment':comment_text }
        comments.append(comment)
        # print(name, ":", comment)
    
    return jsonify({
        'status':200,
        'comments':comments
    })

