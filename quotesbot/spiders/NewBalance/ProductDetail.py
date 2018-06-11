# -*- coding: utf-8 -*-
import scrapy


class NBProductDetail(scrapy.Spider):
    name = "NewBalanceProductDetail"
    start_urls = [
        'https://www.newbalance.com.tr/new-balance-mfl100',
    ]

    def parse(self, response):
        ProductName = response.css("h1.product_title::text").extract_first()

        sizes = []
        for size in response.css("#shoes-sizes tr td::text").extract():
            sizes.append(size)

        pics = []
        for pic in response.css(".nav.nav-tabs li a img").xpath('@src').extract():
            pics.append(pic)

        subCategory = []
        for subcat in response.css(".breadcrumbs a::text").extract():
            if subcat == "Anasayfa":
                pass
            elif subcat == "New Balance":
                pass
            elif subcat in ProductName:
                pass
            else:
                subCategory.append(subcat)




        yield {
                'ProductName': ProductName,
                'ProductDesc': response.css(".short-description").extract_first(),
                'Sizes': sizes,
                'Pictures': pics,
                'SubCategory': subCategory
            }
