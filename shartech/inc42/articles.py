from _typeshed import Self
import re, os, sys
from requests.api import post
import scrapy

import requests
import json, base64, re
from datetime import datetime
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://elite-choice.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=erKx+8XHOGk8i1TlL7WzwphgMVrAFun2EJintn5R1v8="
PAGE_QUEUE = "pages"
ARTICLE_QUEUE = "articles"
SEO_QUEUE = "seo"
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

CNT = int(os.getenv('CNT', 1))

class StartupSpider(scrapy.Spider):
    name = os.getenv('SPIDER', 'articles')

    access_token = ''

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

        # yield scrapy.Request("https://elitechoice.org/luxury/aman-announces-a-new-lifestyle-brand-janu/", self.parse)


    def parse(self, response):
        print(response.url, '\n')

        keyword = response.url.split('/')

        category = keyword[-2]
        print("category: ", category, '\n')

        categories = [category]

        keyword = keyword[-1]
        print(keyword, '\n')

        title = response.css('header.entry-header h1.entry-title::text').get()
        print(title, '\n')

        author = response.css('header.entry-header span.entry-author span.author a::text').get()
        print(author, '\n')

        featured_img = response.css('article.entry-content figure.size-large img').get()
        print(featured_img, '\n')

        content = response.css('article.entry-content').get()
        print(content, '\n')
        # content = featured_img + content

        img_src  = response.css('article.entry-content figure.size-large img').attrib['src']
        img_alt = keyword
        print(img_src, '\n')
        print(img_alt, '\n')

        # tags = response.css('article.post div.tag-list a::text').getall()
        # print(tags, '\n')

        # re_tags = []
        # for tag in tags:
        #     val = re.sub(r'^\s+', "", tag)
        #     val = re.sub(r'\s+$', "", val)
        #     re_tags.append(val)        
        # print(re_tags, '\n')
        # tags = re_tags

        meta_description = response.css('article.entry-content p::text').get()
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


    def test(self):
        url = "https://wordpress.com/post/lavizz.com/2386"