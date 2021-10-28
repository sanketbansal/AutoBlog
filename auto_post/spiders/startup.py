import re, os
from requests.api import post
import scrapy
from selenium import webdriver
# from wrdprs import create_post

import requests
import json, base64, re
from datetime import datetime

class StartupSpider(scrapy.Spider):
    name = "startups"

    start_urls = [
        'https://startuptalky.com/tag/startuptalkers/',
        # 'https://startuptalky.com/tag/insights/',
        # 'https://startuptalky.com/tag/news/',
        # 'https://startuptalky.com/tag/saas/',
        # 'https://startuptalky.com/tag/learning/',
        # 'https://startuptalky.com/tag/successful-company-profiles/'
    ]

    def parse(self, response):
        # article_url = response.css('article a.post-card__media::attr(href)').getall()
        # for url in article_url:
        #      yield response.follow(url, callback=self.parse_article)

        print(response.status, '\n')

        # article_url = response.css('article a.post-card__media::attr(href)').get()
        # yield response.follow(article_url, callback=self.parse_article)

        for page in range(2, 10):
            nextpage_url = re.sub(r'page/\d{1}/', "" ,response.url) + 'page/' + str(page) + '/'
            yield response.follow(nextpage_url, callback=self.parse_next_page)

    def parse_next_page(self,response):
        print(response.status, '\n')
        if(response.status != 200):
            pass
        # article_url = response.css('article a.post-card__media::attr(href)').getall()
        # for url in article_url:
        #      yield response.follow(url, callback=self.parse_article)

        article_url = response.css('article a.post-card__media::attr(href)').get()
        # yield response.follow(article_url, callback=self.parse_article)
