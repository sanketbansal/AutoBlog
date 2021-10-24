import requests
from requests.api import post
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, json, base64, re, time

# from wrdprs import create_post

# Selenium For Post SEO
cwd = os.chdir("C:\\laviz\\auto_post\\seo_post")
service = webdriver.chrome.service.Service('./chromedriver')
service.start()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options = options.to_capabilities()
driver = webdriver.Remote(service.service_url, options)
# driver.get('https://wordpress.com/posts/drafts/lavizz.com')
driver.get('https://wordpress.com/post/lavizz.com/931')
driver.implicitly_wait(1000)

username = driver.find_element_by_css_selector('.login__form-userdata .form-text-input')
username.send_keys('sanketbansal57@gmail.com')
cont_btn = driver.find_element_by_css_selector('.login__form-action .form-button').click()

password = driver.find_element_by_css_selector('.form-password-input .form-text-input')
password.send_keys('sank@1902')
login_btn = driver.find_element_by_css_selector('.login__form-action .form-button').click()

time.sleep(10)

ele = driver.find_element(By.CSS_SELECTOR, '.wpseo-metabox-root input')
print('setting Keyword...', '\n')
ele.send_keys('Startup')

ele = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div[1]/section[1]/div[1]/section[2]/div[4]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]')
print('Setting Meta description...', '\n')
ele.send_keys('BlahBlah!')

ele = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[2]')
ele.click()
print('Publish...', '\n')

ele = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]')
ele.click()
print('Published...', '\n')

time.sleep(10)