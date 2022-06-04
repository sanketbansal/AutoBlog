import requests
from requests.api import post
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, json, base64, re, time, sys

# from wrdprs import create_post
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://luxe-digital.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=zpDv1XhjrgpTutbv3U8NIawhG3Rsxx+bnWX2bJVS9E4="
PAGE_QUEUE = "pages"
ARTICLE_QUEUE = "articles"
SEO_QUEUE = "seo"
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

CNT = int(os.getenv('CNT', 1))
data = ""
with servicebus_client:
    # get the Queue Receiver object for the queue
    receiver = servicebus_client.get_queue_receiver(queue_name=SEO_QUEUE, max_wait_time=5)
    with receiver:
        cnt = 0
        for msg in receiver:
            if cnt == CNT:
                break
            print(str(msg), '\n')
            data = json.loads(str(msg))
            print("Received: " + str(data))
            # complete the message so that the message is removed from the queue
            receiver.complete_message(msg)
            cnt += 1

# Selenium For Post SEO

cwd = sys.argv[1]
print("CWD: ", cwd, "\n")
os.chdir(cwd)

# service = webdriver.chrome.service.Service('./chromedriver.exe')
# service.start()

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options = options.to_capabilities()
# # driver = webdriver.Remote(service.service_url, options)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--disable-dev-shm-usage') 
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

driver.get(data['post_url'])
# driver.get("https://wordpress.com/post/lavizz.com/878")
driver.implicitly_wait(100)

username = driver.find_element(By.CSS_SELECTOR, '.login__form-userdata .form-text-input')
username.send_keys('sanketbansal57@gmail.com')
cont_btn = driver.find_element(By.CSS_SELECTOR, '.login__form-action .form-button').click()

password = driver.find_element(By.CSS_SELECTOR, '.form-password-input .form-text-input')
password.send_keys('sank@1902')
login_btn = driver.find_element(By.CSS_SELECTOR, '.login__form-action .form-button').click()

time.sleep(25)

ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/form/div/div/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[1]/div/input')
print('setting Keyword...', '\n')
ele.send_keys(data['keyword'])
# ele.send_keys("Testing...")

ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/form/div/div/div/div/div[2]/div/div[2]/div/div[4]/div/div/section/div/section[2]/div[4]/div[2]/div[1]/div/div/div/div/div/span')
print('Setting Meta description...', '\n')
ele.send_keys(data['meta_description'])
# ele.send_keys("Testing Meta Description...")

ele = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[2]')
ele.click()
print('Publish...', '\n')

ele = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]')
ele.click()
print('Published...', '\n')

time.sleep(10)