import re, os
import sys
from requests.api import post
import scrapy
import requests
import json, base64, re
from datetime import datetime
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://elite-choice.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=erKx+8XHOGk8i1TlL7WzwphgMVrAFun2EJintn5R1v8="
PAGE_QUEUE = "pages"
ARTICLE_QUEUE = "articles"
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

CNT = int(os.getenv('CNT', 1))
class StartupSpider(scrapy.Spider):
    name = os.getenv('SPIDER', 'pages')

    def start_requests(self):
        # start_urls = [
        #     'https://elitechoice.org/luxury/',
        # ]

        # self.push_page(start_urls)
        # yield scrapy.Request('https://elitechoice.org/luxury/page/2', self.parse)

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
        print(response.url, " ", response.status, '\n')

        if(response.status != 200):
            pass

        article_url = response.css('div.entries article div.entry-image-inner a::attr(href)').getall()
        self.push_article(article_url)

        # print(article_url, "\n")

        match = re.search(r'page/\d{1,}', response.url)
        print(match, '\n')
        nextpage_url = []
        if match == None:
            nextpage_url.append(response.url + '/page/' + '2')
        else:
            match = response.url.split('/')
            print(match[-1], '\n')
            curr_page = int(match[-1])
            nextpage_url.append(re.sub(r'page/\d{1,}', "" ,response.url) + 'page/' + str(curr_page+1))
        self.push_page(nextpage_url)


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