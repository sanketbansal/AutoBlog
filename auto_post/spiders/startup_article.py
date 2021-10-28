import re, os
from requests.api import post
import scrapy

import requests
import json, base64, re
from datetime import datetime

class StartupSpider(scrapy.Spider):
    name = "startups_article"

    start_urls = [
        'https://startuptalky.com/tag/startuptalkers/',
        # 'https://startuptalky.com/tag/insights/',
        # 'https://startuptalky.com/tag/news/',
        # 'https://startuptalky.com/tag/saas/',
        # 'https://startuptalky.com/tag/learning/',
        # 'https://startuptalky.com/tag/successful-company-profiles/'
    ]

    access_token = ''
    site_id = 176416011
    # site_id = 0

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

    def parse_article(self, response):
        print(response.url, '\n')

        title = response.css('div.hero__content h1.hero__title::text').get()
        # print(title, '\n')

        author = response.css('div.hero__content div.author-mini a').attrib['title']
        # print(author, '\n')

        featured_img = response.css('div.hero div.hero__media').get()
        # print(featured_img)

        img_src  = response.css('div.hero div.hero__media img.hero__img').attrib['src']
        img_alt = response.css('div.hero div.hero__media img.hero__img').attrib['alt']
        print(img_src, '\n')
        print(img_alt, '\n')

        tags = response.css('article.post div.tag-list a::text').getall()
        print(tags, '\n')

        re_tags = []
        for tag in tags:
            val = re.sub(r'^\s+', "", tag)
            val = re.sub(r'\s+$', "", val)
            re_tags.append(val)        
        print(re_tags, '\n')
        tags = re_tags

        content = response.css('article.post div.content').get()
        # print(content, '\n')

        # wordprs_content = featured_img + content
        wordprs_content = content
        # print(wordprs_content, '\n')

        # params = { 'media_urls': [img_src] }
        # media_id = self.new_media(params)

        # params = { 'alt': img_alt }
        # self.edit_media(params, media_id)

        # categories = ['startups']

        # params = {
        #     'date_gmt': datetime.now().replace(microsecond=0).isoformat() + "Z",
        #     'status': 'draft',
        #     'title': title,
        #     'content': content,
        #     'tags': tags,
        #     'categories': categories,
        #     'featured_image': str(media_id)
        # }
        # post_id = self.create_post(params)

        # params = { 'post_ID': post_id }
        # self.edit_media(params, media_id)
        # self.get_media(media_id)

        # params = { 'featured_image': str(media_id) }
        # self.edit_post(params, post_id)