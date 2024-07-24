from flask import Blueprint,request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import urlparse, parse_qs

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/linkedin', methods=['GET'])
def scrape_comments_linkedin():
    driver = webdriver.Chrome()
    post_url = request.args.get('url')  
    driver.get(post_url)

    time.sleep(1)

    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    comment_body = soup.find_all('div',class_='comment__body')
    comments = []
    for comment in comment_body:
        user = comment.div.a.text.strip()
        comment_text = comment.find_all('p', class_='comment__text')[0].text.strip()
        comment = { 'user':user, 'comment': comment_text }
        comments.append(comment)


    return jsonify({ 
        'status':200,
        'comments': comments
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

