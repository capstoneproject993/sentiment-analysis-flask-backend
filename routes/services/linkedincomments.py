from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def init_linkedin_scrapper():
    linkedin_email = "capstoneproject993@gmail.com"
    linkedin_password = "CapstoneProject#$1"

    driver = webdriver.Edge()


    login_url = 'https://www.linkedin.com/login'

    driver.get(login_url)

    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(linkedin_email)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(linkedin_password)

    password_input.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-identity-module__actor-meta")))
    except Exception as e:
        print("Login failed or feed element not found:", e)
        driver.quit()
        exit()
    return driver

def get_linkedin_comments(url, driver):
    driver.get(url)
    try:
        most_recent_drop = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.comments-sort-order-toggle__trigger"))
        )
        most_recent_drop.click()
        most_recent_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.comments-sort-order-toggle-option"))
        )
        for option in most_recent_btn:
            if "Most recent" in option.text:
                option.click()
                break
    except:
        pass

    def load_all_comments():
        while True:
            try:
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.comments-comments-list__show-previous-container button"))
                )
                load_more_button.click()
                time.sleep(2)
            except:
                break

    load_all_comments()

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    comment_body = soup.find_all('article',class_='comments-comment-item')    
    comments = []

    for comment in comment_body:
        user = comment.findAll('span',class_='comments-post-meta__name-text')[0].text.strip()
        comm = comment.find_all('div', class_='comments-comment-item-content-body')
        if(len(comm)!=0):
            comment_text = comm[0].text.strip()
            comment_data = {
                'user': user,
                'comment': comment_text
            }
            comments.append(comment_data)

    return comments