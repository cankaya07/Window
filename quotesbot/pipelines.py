
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import os
import re
import requests
import pymongo

from urllib.parse import urljoin
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.conf import settings
from bson.objectid import ObjectId  


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item





class DefaultValuePipeline(object):

    def process_item(self, item, spider):
        item.setdefault('comment', '')
        item.setdefault('source_url', '')
        item.setdefault('image_urls', [])

        return item


class DuplicatePipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['source_url'] in self.urls_seen:
            raise DropItem('Duplicate item found: %s' % item['source_url'])
        else:
            self.urls_seen.add(item['source_url'])

            return item


class NormalizationPipeline(object):

    def process_item(self, item, spider):
        blogspot_image_re = re.compile(r'/s\d+/', re.IGNORECASE)

        if len(item['image_urls']) == 0:
            raise DropItem('No image found: %s' % item['source_url'])

        comment = item['comment']
        if isinstance(comment, list):
            try:
                comment = comment[0]
            except IndexError:
                comment = ''
        item['comment'] = comment.strip()

        if spider.name == 'atlanticpacific':
            new_image_urls = []
            for image_url in item['image_urls']:
                if blogspot_image_re.search(image_url):
                    bigger_image_url = blogspot_image_re.sub('/s1600/', image_url)
                    new_image_urls.append(bigger_image_url)
            item['image_urls'] = new_image_urls

        elif spider.name == 'beautylegmm':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = urljoin('http://www.beautylegmm.com/', image_url)
                new_image_urls.append(new_image_url)
            item['image_urls'] = new_image_urls

        elif spider.name == 'carolinakrews':
            new_image_urls = []
            for image_url in item['image_urls']:
                if blogspot_image_re.search(image_url):
                    bigger_image_url = blogspot_image_re.sub('/s1600/', image_url)
                    new_image_urls.append(bigger_image_url)
            item['image_urls'] = new_image_urls

        elif spider.name == 'garypeppergirl':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = re.sub(r'\-\d+x\d+\.', '.', image_url)
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'itscamilleco':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = re.sub(r'\-\d+x\d+\.', '.', image_url)
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'pinterest':
            item['source_url'] = item['source_url'].replace('https://', 'http://')

            if comment.startswith(('. | ', '| ')):
                item['comment'] = comment.replace('. | ', '').replace('| ', '')

            new_image_urls = []
            for image_url in item['image_urls']:
                if filter(image_url.endswith, ('.jpg', '.jpeg', '.gif', '.png')):
                    ori_image_url = image_url.replace('736x', 'originals')
                    new_image_urls.append(ori_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'seemodel':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = 'http://www.seemodel.com/' + image_url
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        elif spider.name == 'wendyslookbook':
            new_image_urls = []
            for image_url in item['image_urls']:
                new_image_url = re.sub(r'\-\d+x\d+\.', '.', image_url)
                new_image_urls.append(new_image_url)

            item['image_urls'] = new_image_urls

        item['image_urls'] = list(set(item['image_urls']))

        return item


class SubmitItemPipeline(object):

    def process_item(self, item, spider):
        TOKEN = os.environ['HF_TOKEN']
        API_URL = os.environ['HF_SUBMIT_API_URL']

        headers = {
            'Authorization': 'Token %s' % (TOKEN),
        }
        payload = {
            'name': spider.name,
            'url': spider.start_urls[0],
            'item': dict(item),
        }
        r = requests.post(API_URL, data=json.dumps(payload), headers=headers)
        if not r.ok:
            log.msg(r.content, level=log.ERROR)

        return item