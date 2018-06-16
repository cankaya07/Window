# -*- coding: utf-8 -*-
import scrapy
import json
from quotesbot.Classes import Product
from quotesbot.Classes import BreadCrumbCategory
from quotesbot.Classes import Price
from quotesbot.Classes import VariantColors
from bs4 import BeautifulSoup



class RBProductListPage(scrapy.Spider):
    name = "ReebokProductListPage"
    start_urls = [
        'https://www.reebok.com.tr/erkek-spor-ayakkabi?ps=5000',
    ]

    def parse(self, response):
        cnt = len(response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div'))
        for i in range(1,cnt):
            quote=response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div['+str(i)+']/div')
            item = Product()
            p = Price()
            extra_info = response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/script['+str(i)+']/text()').extract_first()
            extra_info = extra_info.replace("'",'"').replace("impressionList.push(data);","").replace(" data =","[").replace("};","").strip()
            extra_info= extra_info[:-1].replace('"position":','"position": "')+'"}]'
            j = json.loads(extra_info)

            p["Currency"]="TL"
            
            PriceWithoutDiscount = quote.xpath('./div/div[5]/div[4]/p[2]/span/text()').extract_first()
            if PriceWithoutDiscount is not None:
                p["PriceWithDiscount"]=float(j[0]["price"])
                p["Price"] = float(PriceWithoutDiscount.replace(",",".").replace("TL",""))
                p["DiscountPerc"] = (p["Price"]-p["PriceWithDiscount"])*100/p["Price"]
            else:
                p["Price"]=j[0]["price"]
            
            categoryList = []
            for x in str(j[0]["category"]).split("/"):
                c = BreadCrumbCategory()
                c["Name"] = x
                categoryList.append(c)

            #Extra Category Name like running shoe
            c = BreadCrumbCategory()
            c["Name"] = response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div['+str(i)+']/div/div[5]/div[3]/text()').extract_first()
            categoryList.append(c)

            item["Code"] = j[0]["id"]
            item["Name"]=j[0]["name"]
            item["url"] =  response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div['+str(i)+']/div/div[3]/a/@href').extract_first()
            item["Price"] = p
            item["Category"] = categoryList
            item["SiteName"] = "ReebokOfficial"
            yield item