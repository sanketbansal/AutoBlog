#! /bin/bash

# ls -a
scrapy startproject auto_post
mv $SPIDER.py auto_post/auto_post/spiders/$SPIDER.py
cd auto_post
cd auto_post
# ls -a
cd spiders
# ls -a
cd ..
scrapy crawl $SPIDER