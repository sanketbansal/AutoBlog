import re, os
import sys
from requests.api import post
import scrapy
import requests
import json, base64, re
from datetime import datetime

from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://lavizz.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=oQxdnzaJpswC8m0C2FSkloe/b5m5gb+l74jC3lz/vCA="
PAGE_QUEUE = "pages"
ARTICLE_QUEUE = "articles"
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

CNT = int(os.getenv('CNT', 1))
class StartupSpider(scrapy.Spider):
    name = os.getenv('SPIDER', 'pages')

    def start_requests(self):
        # start_urls = [
        #     'https://startuptalky.com/tag/startuptalkers/',
        #     'https://startuptalky.com/tag/insights/',
        #     'https://startuptalky.com/tag/news/',
        #     'https://startuptalky.com/tag/saas/',
        #     'https://startuptalky.com/tag/learning/',
        #     'https://startuptalky.com/tag/successful-company-profiles/'
        # ]

        # self.push_page(start_urls)

        url = ""
        with servicebus_client:
            # get the Queue Receiver object for the queue
            receiver = servicebus_client.get_queue_receiver(queue_name=PAGE_QUEUE, max_wait_time=5)
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


    def parse(self, response):
        print(response.status, '\n')

        if(response.status != 200):
            pass

        article_url = response.css('article a.post-card__media::attr(href)').getall()
        urls = []
        for url in article_url:
            urls.append('https://startuptalky.com' + url)
        self.push_article(urls)

        # for url in article_url:
        #      yield response.follow(url, callback=self.parse_article)

        match = re.search(r'page/\d{1,}/', response.url)
        print(match, '\n')
        nextpage_url = []
        if match == None:
            nextpage_url.append(response.url + 'page/' + '2' + '/')
        else:
            match = response.url.split('/')
            print(match[-2], '\n')
            curr_page = int(match[-2])
            nextpage_url.append(re.sub(r'page/\d{1,}/', "" ,response.url) + 'page/' + str(curr_page+1) + '/')
        self.push_page(nextpage_url)
        # for url in nextpage_url:
        #     yield response.follow(url, callback=self.parse)


    def push_page(self, page_url):
        with servicebus_client:
            # get a Queue Sender object to send messages to the queue
            sender = servicebus_client.get_queue_sender(queue_name=PAGE_QUEUE)
            with sender:
                for url in page_url:
                    message = ServiceBusMessage(url)
                    sender.send_messages(message)

    def push_article(self, article_url):
        with servicebus_client:
            # get a Queue Sender object to send messages to the queue
            sender = servicebus_client.get_queue_sender(queue_name=ARTICLE_QUEUE)
            print(article_url, '\n')

            with sender:
                for url in article_url:
                    message = ServiceBusMessage(url)
                    sender.send_messages(message)