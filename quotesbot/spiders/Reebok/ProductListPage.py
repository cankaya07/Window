# -*- coding: utf-8 -*-
import scrapy
import json


class RBProductListPage(scrapy.Spider):
    name = "ReebokProductListPage"
   
    start_urls = [
        "https://www.reebok.com.tr/erkek-spor-ayakkabi?ps=5000"
    ]

    def parse(self, response):
        for quote in response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div'):
            yield {
                'ProductName': quote.xpath('./div/div[5]/div[2]/a/text()').extract_first(),
                'ProductUrl': self.start_urls[0]+quote.xpath('./div/div[5]/div[2]/a/@href').extract_first(),
                'OnClick': self.start_urls[0]+quote.xpath('./div/div[5]/div[2]/a/@onlick').extract_first(),
            }