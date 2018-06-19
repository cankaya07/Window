# -*- coding: utf-8 -*-
import scrapy,json
from quotesbot.Classes import Product
from quotesbot.Classes import Size
from quotesbot.Classes import Picture
from quotesbot.Classes import BreadCrumbCategory
from pymongo import MongoClient
from bs4 import BeautifulSoup

class ADDProductDetail(scrapy.Spider):
    name = "AdidasProductDetail"

    def start_requests(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['Vitrin']
        collection = db['Sites']
        for obj in collection.find({"SiteName": 'AdidasOfficial'}):
            p = Product()
            p= obj
            yield scrapy.Request('https://shop.adidas.com.tr'+obj["url"], meta={'item':p})

    def parse(self, response):
        item = response.meta['item']
        
        sizes = []
        for size in response.css(".size-list li a").extract():
            a = BeautifulSoup(size, "lxml").find('a', class_="")
            if a is not None:
                s = Size()
                s["SizeName"]=a.text
                s["SizeStock"]=a["data-stock"]
                sizes.append(s)

        pics = []
        for pic in response.css("#thumblist li a img").extract():
            soup = BeautifulSoup(pic, "lxml")
            p=Picture()
            p["PicturePath"]=soup.find('img')["src"]
            pics.append(p)

        sCategory = []
        for subCategory in response.css("#breadcrumbs ul li a").extract():
            soup = BeautifulSoup(subCategory, "lxml")
            subcat=  BeautifulSoup(soup.find('a').text, "lxml").text
            if subcat == "Anasayfa":
                pass
            elif subcat == "Geri":
                pass
            elif subcat == item["Name"]:
                pass
            else:
                b = BreadCrumbCategory()
                b["Name"]= subcat
                b["Url"]= '/'+soup.find('a')["href"]
                sCategory.append(b)

        desc=""
        d = response.xpath('//*[@id="product-body"]/div[3]/div/div[1]/div[2]/p/text()').extract_first()
        if d is not None:
            desc = d +"<br/>"
        d = response.xpath('//*[@id="product-body"]/div[3]/div/div[1]/div[3]').extract_first()
        if d is not None:
            desc = desc + d
          
        item["Desc"]= desc
        item['Size']= sizes
        item['Picture'] = pics
        item['SubCategory'] = sCategory
        yield item