# -*- coding: utf-8 -*-
import scrapy
import json
from quotesbot.Classes import Product
from quotesbot.Classes import BreadCrumbCategory
from quotesbot.Classes import Price
from quotesbot.Classes import VariantColors
from bs4 import BeautifulSoup



class ADDSProductListPage(scrapy.Spider):
    name = "AdidasProductListPage"
    start_urls = [
        'https://shop.adidas.com.tr/erkek-ayakkabi?ps=5000',
    ]

    def parse(self, response):
        for quote in response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div'):
            item = Product()
            p = Price()
            extra_info = quote.xpath('./@data-prop').extract_first()
            if extra_info is not None:
                item["Code"] = extra_info.split('|')[1]
                p["PriceWithDiscount"] = float(extra_info.split('|')[2].replace(".","").replace(",","."))
                p["Price"] = float(extra_info.split('|')[3])
                p["DiscountPerc"] = (p["Price"]-p["PriceWithDiscount"])*100/p["Price"]

            p["Currency"]="TL"
            
            categoryList = []
            for x in extra_info.split('|')[6].split(">"):
                c = BreadCrumbCategory()
                c["Name"] = x
                categoryList.append(c)

            #Extra Category Name like running shoe
            c = BreadCrumbCategory()
            c["Name"] = extra_info.split('|')[4]
            categoryList.append(c)

            a = BeautifulSoup(quote.xpath('./div/div[5]/div[2]/a').extract_first(), "lxml").find('a')
            item["Name"]= a.text
            item["url"] = a["href"]
            item["Price"] = p
            item["Category"] = categoryList
            item["SiteName"] = "AdidasOfficial"
            yield item