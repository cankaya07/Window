# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from bs4 import BeautifulSoup
from quotesbot.Classes import Size, Picture, BreadCrumbCategory, Price,VariantColors, Product

class ADDSProductListPage(Spider):
    name = "KoraySporProductListPage"
    start_urls = [
        'https://www.korayspor.com/erkek-spor-ayakkabi/',
    ]
    
    def parse(self, response):
        sel = Selector(response)
        contents = sel.xpath('//*[@id="ajxUrunList"]/div/ul')

        for products in contents.xpath('//*[@id="ajxUrunList"]/div/ul/li'):
            item = Product()
            p = Price()
            _pName = BeautifulSoup(products.css('.ems-prd-name').extract_first(), "lxml").find('a')
            item["Name"]= _pName.text
            item["url"] = _pName["href"].strip()
            item["SiteName"] = "KoraySpor"
            p["Currency"]= products.css('.pb1::text').extract_first()
            item["Code"] = products.css('.ems-prd-code.ems-hidden').xpath('./a/text()').extract_first()
            p["PriceWithDiscount"] = float(products.css('.urunListe_satisFiyat::text').extract_first())


            extra_info = products.css('.urunListe_brutFiyat').extract_first()
            if extra_info is not None:
                p["Price"] = float(products.css('.urunListe_brutFiyat::text').extract_first())
                p["DiscountPerc"] = (p["Price"]-p["PriceWithDiscount"])*100/p["Price"]
           
           
            c = BreadCrumbCategory()
            c["Name"] = products.css('.ems-prd-name-cat a::text').extract_first()
            item["Price"] = p
            item["Category"] = c

            yield item

        #paging part
        aElement = BeautifulSoup(str(sel.css('.urunPaging_pageNavigation a').extract()), "lxml").find("a",id=lambda value: value and value.endswith("_lnkNext"))
        if aElement is not None:
            if aElement.find("span").text == ">>":
                yield Request('https://www.korayspor.com'+str(aElement["href"]))
                #yield Request('https://www.korayspor.com'+str(aElement["href"]))
    
    def parse_details(self,response):
        self.log(response)
        item = response.meta['item']
        
        sel = Selector(response)
        sizes = []
        for size in sel.css("#dropdown-options-scd1-urunDetay0 a div::text").extract():
            self.log(size)
            s = Size()
            s["SizeName"]=size
            sizes.append(s)

        pics = []
        for pic in sel.css("ul.swiper-wrapper.slide-wrp li.swiper-slide").extract():
            self.log(pic)
            soup = BeautifulSoup(pic, "lxml")
            p=Picture()
            p["PictureName"]=soup.find('img')["alt"]
            p["PicturePath"]=soup.find('img')["src"]
            pics.append(p)
        
        # # item["Desc"]= response.css(".short-description").extract_first()
        item['Size']= sizes
        item['Picture'] = pics
        # # item['SubCategory'] = sCategory
        
        return item
        
 

    # def __to_absolute_url(self, base_url, link):
    #     import urlparse
	# 	return urlparse.urljoin(base_url, link)

    # def parse_details(self, response):
    #     sel = Selector(response)
    #     console.log('GİRDİ')
    #     film = sel.xpath('//div[@id="content-2-wide"]')
    #     return

		# # Populate film fields
		# item = ScrapyTutorialItem()
		# item['title'] = film.xpath('.//h1/span[contains(@class, "itemprop")]/text()').extract()
		# item['year'] = film.xpath('.//div[@id="ratingWidget"]/p[1]/strong/following-sibling::node()').extract()
		# item['rating'] = film.xpath('.//span[@itemprop="ratingValue"]/text()').extract()
		# item['num_of_nominations'] = film.xpath('.//*[@itemprop="awards"][contains(., "nominations")]/text()').extract()
		# item['description'] = film.xpath('.//p[@itemprop="description"]/text()').extract()
		# item['poster_url'] = film.xpath('.//*[@id="img_primary"]//img/@src').extract()
		# item['film_url'] = response.url
		# item = self.__normalise_item(item, response.url)

		# # Get films with at least 5 award nominations
		# if item['num_of_nominations'] >= 5:
		# 	return item

	# def __normalise_item(self, item, base_url):
	# 	'''
	# 	Standardise and format item fields
	# 	'''

	# 	# Loop item fields to sanitise data and standardise data types
	# 	for key, value in vars(item).values()[0].iteritems():
	# 		item[key] = self.__normalise(item[key])

	# 	# Clean year and convert year from string to float
	# 	item['year'] = item['year'].strip('()')
	# 	item['type'] = 'Movie'

	# 	if len(item['year']) > 4:
	# 		item['type'] = 'TV Series'
	# 		item['year'] = item['year'][0:4]
	# 	item['year'] = self.__to_int(item['year'])

	# 	# Convert rating from string to float
	# 	item['rating'] = self.__to_float(item['rating'])

	# 	# Convert no. of nominations from string to int
	# 	if item['num_of_nominations']:
	# 		item['num_of_nominations'] = item['num_of_nominations'].split('&')[1]
	# 		item['num_of_nominations'] = [int(s) for s in item['num_of_nominations'].split() if s.isdigit()][0]
	# 	else:
	# 		item['num_of_nominations'] = 0

	# 	# Convert film URL from relative to absolute URL
	# 	item['film_url'] = self.__to_absolute_url(base_url, item['film_url'])

	# 	return item

	# def __normalise(self, value):
	# 	# Convert list to string
	# 	value = value if type(value) is not list else ' '.join(value)
	# 	# Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
	# 	value = value.strip()

	# 	return value



	# def __to_int(self, value):
	# 	'''
	# 	Convert value to integer type
	# 	'''

	# 	try:
	# 		value = int(value)
	# 	except ValueError:
	# 		value = 0

	# 	return value

	# def __to_float(self, value):
	# 	'''
	# 	Convert value to float type
	# 	'''

	# 	try:
	# 		value = float(value)
	# 	except ValueError:
	# 		value = 0.0

	# 	return value



        # for quote in response.xpath('//*[@id="department-body"]/div/div[2]/div[3]/div'):
        #     item = Product()
        #     p = Price()
        #     extra_info = quote.xpath('./@data-prop').extract_first()
        #     if extra_info is not None:
        #         item["Code"] = extra_info.split('|')[1]
        #         p["PriceWithDiscount"] = float(extra_info.split('|')[2].replace(".","").replace(",","."))
        #         p["Price"] = float(extra_info.split('|')[3])
        #         p["DiscountPerc"] = (p["Price"]-p["PriceWithDiscount"])*100/p["Price"]

        #     p["Currency"]="TL"
            
        #     categoryList = []
        #     for x in extra_info.split('|')[6].split(">"):
        #         c = BreadCrumbCategory()
        #         c["Name"] = x
        #         categoryList.append(c)

        #     #Extra Category Name like running shoe
        #     c = BreadCrumbCategory()
        #     c["Name"] = extra_info.split('|')[4]
        #     categoryList.append(c)

        #     a = BeautifulSoup(quote.xpath('./div/div[5]/div[2]/a').extract_first(), "lxml").find('a')
        #     item["Name"]= a.text
        #     item["url"] = a["href"]
        #     item["Price"] = p
        #     item["Category"] = categoryList
        #     item["SiteName"] = "KoraySpor"
        #     yield item