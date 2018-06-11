# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import json

   


class NBMainCategories(scrapy.Spider):
    name = "NewBalanceMainCategories"
    start_urls = [
        'https://www.newbalance.com.tr/',
    ]

    def parse(self, response):
        Header = ["CategoryName","CategoryUrl"]
        CategoryName=list(response.css("#mega_main_menu_ul_first").xpath(".//li").xpath(".//a//span//span/text()").extract())
        CategoryUrl=list(response.css("#mega_main_menu_ul_first").xpath(".//li").xpath(".//a/@href").extract())

        with open('NBMainCategories.json', 'w') as outfile:
            json.dump(json.dumps([dict(zip(Header, row)) for row in zip(CategoryName,CategoryUrl)], indent=1), outfile)
