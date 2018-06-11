# -*- coding: utf-8 -*-
import scrapy
import json


class NBProductListPage(scrapy.Spider):
    name = "NewBalanceProductListPage"
    with open('NBMainCategories.json') as MainUrls:
        data = json.load(MainUrls)
    start_urls = list(data[0])

    def parse(self, response):
        jsonoutput = []
        for quote in response.xpath('//*[@id="grid"]/div[1]/div'):
            yield {
                'ProductName': quote.xpath('./div/div[2]/a/text()').extract_first(),
                'ProductUrl': self.start_urls[0]+quote.xpath('./div/div[2]/a/@href').extract_first(),
            }

        CurrentPageNumber = response.css("ul.page-numbers li span.page-numbers.current::text").extract_first()
        LastPage = response.css("ul.page-numbers li:nth-last-child(2) a.page-numbers::text").extract_first()
        if LastPage is None:
            LastPage=CurrentPageNumber

        if int(CurrentPageNumber) < int(LastPage):
            yield scrapy.Request(response.urljoin('?page='+str(int(CurrentPageNumber)+1)))
