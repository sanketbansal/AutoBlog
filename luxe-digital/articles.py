import re, os, sys
from requests.api import post
import scrapy

import requests
import json, base64, re
from datetime import datetime
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://luxe-digital.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=zpDv1XhjrgpTutbv3U8NIawhG3Rsxx+bnWX2bJVS9E4="
PAGE_QUEUE = "pages"
ARTICLE_QUEUE = "articles"
SEO_QUEUE = "seo"
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

CNT = int(os.getenv('CNT', 1))

class StartupSpider(scrapy.Spider):
    name = os.getenv('SPIDER', 'articles')

    access_token = ''
    site_id = 176416011

    def start_requests(self):
        url = ""
        with servicebus_client:
            # get the Queue Receiver object for the queue
            receiver = servicebus_client.get_queue_receiver(queue_name=ARTICLE_QUEUE, max_wait_time=5)
            with receiver:
                cnt = 0
                for msg in receiver:
                    if cnt == CNT:
                        break
                    url = str(msg)
                    print("Received: " + url)
                    # complete the message so that the message is removed from the queue
                    receiver.complete_message(msg)
                    cnt += 1
                    yield scrapy.Request(url, self.parse)

    def authenticate(self):
        auth = {
            'client_id': '77453',
            'client_secret': '7b9RDuBX8kaLWQ2bt7d2EsSJGOww7BVDSQx3KdzNbP9bUYI4i4gU3kW0YAMMUk5G',
            'grant_type': 'password',
            'username': 'sanketbansal57',
            'password': 'sank@1902',
        }

        # auth = {
        #     'client_id': '77453',
        #     'client_secret': '7b9RDuBX8kaLWQ2bt7d2EsSJGOww7BVDSQx3KdzNbP9bUYI4i4gU3kW0YAMMUk5G',
        #     'redirect_uri': 'https://lavizz.com/',
        #     'code': 'XjNDL5cUuk',
        #     'grant_type':'authorization_code'
        # }

        response = requests.post('https://public-api.wordpress.com/oauth2/token', data=auth).json()
        print(response, '\n')
        self.access_token = response['access_token']

        # https://lavizz.com/#access_token=%23J%235%23%29Uh8XJHbiClXCqEKnH3Xs%5ETrIz15xqM2H32yKfFfUtTe%40fLr5KNe%24NM6sDe&expires_in=1209600&token_type=bearer&site_id=0&scope=global
        # site_id = 176416011 // LAVIZ

    def create_post(self, params):

        if(self.access_token == ''):
            print("Authenticating....", '\n')
            self.authenticate()
            print(self.access_token, "\n")

        header = {'Authorization': 'Bearer ' + self.access_token}

        wordpress_url = 'https://public-api.wordpress.com/rest/v1.2/sites/' + str(self.site_id) + '/posts/new/'
        response = requests.post(wordpress_url, headers=header, data=params)

        print("Posting....", '\n')
        print(response.json(), '\n')
        return response.json()['ID']

    def edit_post(self, params, post_id):
        if(self.access_token == ''):
            print("Authenticating....", '\n')
            self.authenticate()
            print(self.access_token, "\n")

        header = {'Authorization': 'Bearer ' + self.access_token}

        wordpress_url = 'https://public-api.wordpress.com/rest/v1.2/sites/' + str(self.site_id) + '/posts/' + str(post_id)
        response = requests.post(wordpress_url, headers=header, data=params)

        print("Editing Post....", '\n')
        print(response.json(), '\n')

    def new_media(self, params):

        if(self.access_token == ''):
            print("Authenticating....", '\n')
            self.authenticate()
            print(self.access_token, "\n")

        header = {'Authorization': 'Bearer ' + self.access_token}

        wordpress_url = 'https://public-api.wordpress.com/rest/v1.1/sites/' + str(self.site_id) + '/media/new/'
        response = requests.post(wordpress_url, headers=header, data=params)

        print("Uploading Media....", '\n')
        print(response, '\n')
        id = response.json()['media'][0]['ID']
        return id

    def edit_media(self, params, id):

        if(self.access_token == ''):
            print("Authenticating....", '\n')
            self.authenticate()
            print(self.access_token, "\n")

        header = {'Authorization': 'Bearer ' + self.access_token}
        wordpress_url = 'https://public-api.wordpress.com/rest/v1.1/sites/' + str(self.site_id) + '/media/' + str(id) + '/'
        response = requests.post(wordpress_url, headers=header, data=params)

        print("Editing Media....", '\n')
        print(response, '\n')

    def get_media(self, id):
        if(self.access_token == ''):
            print("Authenticating....", '\n')
            self.authenticate()
            print(self.access_token, "\n")

        header = {'Authorization': 'Bearer ' + self.access_token}
        wordpress_url = 'https://public-api.wordpress.com/rest/v1.1/sites/' + str(self.site_id) + '/media/' + str(id) + '/'
        response = requests.get(wordpress_url, headers=header)

        print("Fetching Media....", '\n')
        print(response.json(), '\n')

    def parse(self, response):
        print(response.url, '\n')

        keyword = response.url.split('/')
        keyword = keyword[-2]
        print(keyword, '\n')

        title = response.css('header.entry-header h1.entry-title::text').get()
        # print(title, '\n')

        category = response.css('header.entry-header p.entry-meta span.entry-categories a::text').get()
        # print(category, '\n')

        categories = [category]

        author = response.css('header.entry-header p.entry-meta span.entry-author span.entry-author-name::text').get()
        # print(author, '\n')

        featured_img = response.css('header.entry-header img.attachment-post-image').get()
        # print(featured_img)

        content = response.css('main.content article div.entry-content').get()
        # print(content, '\n')
        content = featured_img + content

        img_src  = response.css('header.entry-header img.attachment-post-image').attrib['src']
        img_alt = response.css('header.entry-header img.attachment-post-image').attrib['alt']
        # print(img_src, '\n')
        # print(img_alt, '\n')

        # tags = response.css('article.post div.tag-list a::text').getall()
        # print(tags, '\n')

        # re_tags = []
        # for tag in tags:
        #     val = re.sub(r'^\s+', "", tag)
        #     val = re.sub(r'\s+$', "", val)
        #     re_tags.append(val)        
        # print(re_tags, '\n')
        # tags = re_tags

        meta_description = response.css('main.content article div.entry-content p::text').get()
        meta_description = meta_description[:120] + "..."
        print(meta_description, '\n')

        params = { 'media_urls': [img_src] }
        media_id = self.new_media(params)

        params = { 'alt': img_alt }
        self.edit_media(params, media_id)

        params = {
            'date_gmt': datetime.now().replace(microsecond=0).isoformat() + "Z",
            'status': 'draft',
            'title': title,
            'content': content,
            'categories': categories,
            'featured_image': str(media_id)
        }
        post_id = self.create_post(params)

        params = { 'post_ID': post_id }
        self.edit_media(params, media_id)
        # self.get_media(media_id)

        params = { 'featured_image': str(media_id) }
        self.edit_post(params, post_id)

        site_post_url = 'https://wordpress.com/post/lavizz.com/'
        seo_data = {
            'post_url': site_post_url + str(post_id),
            'keyword': keyword,
            'meta_description': meta_description
        }
        seo_data = json.dumps(seo_data)
        self.push_seo([seo_data])

    def push_seo(self, datas):
        with servicebus_client:
            # get a Queue Sender object to send messages to the queue
            sender = servicebus_client.get_queue_sender(queue_name=SEO_QUEUE)
            with sender:
                for seo_data in datas:
                    message = ServiceBusMessage(seo_data)
                    sender.send_messages(message)