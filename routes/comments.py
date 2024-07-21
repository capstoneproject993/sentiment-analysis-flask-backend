from flask import Blueprint,request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

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


