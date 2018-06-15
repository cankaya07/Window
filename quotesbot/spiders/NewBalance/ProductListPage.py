# -*- coding: utf-8 -*-
import scrapy
import json
from quotesbot.Classes import Product


class NBProductListPage(scrapy.Spider):
    name = "NewBalanceProductListPage"
    start_urls = [
        "https://newbalance.com.tr/erkek-ayakkabi",
        ]
   

    def parse(self, response):
        for quote in response.xpath('//*[@id="grid"]/div[1]/div'):
            item = Product()
            item['Code'] = quote.xpath('./div/div[2]/a/text()').extract_first()
            item['url'] = quote.xpath('./div/div[2]/a/@href').extract_first()
            item['SiteName'] = "NewBalanceOfficial"
            yield item

        CurrentPageNumber = response.css("ul.page-numbers li span.page-numbers.current::text").extract_first()
        LastPage = response.css("ul.page-numbers li:nth-last-child(2) a.page-numbers::text").extract_first()
        if LastPage is None:
            LastPage=CurrentPageNumber

        if int(CurrentPageNumber) < int(LastPage):
            yield scrapy.Request(response.urljoin('?page='+str(int(CurrentPageNumber)+1)))
