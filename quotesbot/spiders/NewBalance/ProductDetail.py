# -*- coding: utf-8 -*-
import scrapy,json
from quotesbot.Classes import Product
from quotesbot.Classes import Size
from quotesbot.Classes import Picture
from quotesbot.Classes import BreadCrumbCategory
from pymongo import MongoClient
from bs4 import BeautifulSoup

class NBProductDetail(scrapy.Spider):
    name = "NewBalanceProductDetail"

    def start_requests(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['Vitrin']
        collection = db['Sites']
        for obj in collection.find({"SiteName": 'NewBalanceOfficial'}):
            p = Product()
            p= obj
            yield scrapy.Request('https://www.newbalance.com.tr'+obj["url"], meta={'item':p})

    def parse(self, response):
        item = response.meta['item']
        item["Name"] = response.css("h1.product_title::text").extract_first()

        sizes = []
        for size in response.css("#shoes-sizes tr td::text").extract():
            s = Size()
            s["SizeName"]=size
            sizes.append(s)

        pics = []
        for pic in response.css(".nav.nav-tabs li a img").extract():
            soup = BeautifulSoup(pic, "lxml")
            p=Picture()
            p["PictureName"]=soup.find('img')["title"]
            p["PicturePath"]=soup.find('img')["src"]
            pics.append(p)

        sCategory = []
        for subCategory in response.css(".breadcrumbs a").extract():
            soup = BeautifulSoup(subCategory, "lxml")
            subcat= soup.find('a').text
            if subcat == "Anasayfa":
                pass
            elif subcat == "New Balance":
                pass
            elif subcat == item["Name"]:
                pass
            else:
                b = BreadCrumbCategory()
                b["Name"]= subcat
                b["Url"]= soup.find('a')["href"]
                sCategory.append(b)

        
        item["Desc"]= response.css(".short-description").extract_first()
        item['Size']= sizes
        item['Picture'] = pics
        item['SubCategory'] = sCategory
        yield item