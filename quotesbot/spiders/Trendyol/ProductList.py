from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
from bs4 import BeautifulSoup
from quotesbot.Classes import Size, Picture, BreadCrumbCategory, Price,VariantColors, Product
from scrapy_splash import SplashRequest
import inspect
from quotesbot.Tools import PrepareJSONDoubleQuoteProblem
import json
 
 
 
class TrendYolProductListPage(CrawlSpider):
    name = "TrendyolProductListPage"
    allowed_domains = ['www.trendyol.com', ]
    start_urls = [
        'https://www.trendyol.com/erkek+giyim?qs=navigation',]

    rules = (
        # find next page
        Rule(
            LinkExtractor(
                allow=(r'erkek+ayakkabi?qs=navigation&pi\d+', ),
                restrict_css=('.pagination', ),
                unique=True,
            ),
            
            follow=True,
        ),
        # go detail page
        Rule(
            LinkExtractor(
                restrict_css=('.row.products', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

  
   
 
    def parse_post_detail(self, response):
        """
    Scrapy creates scrapy.http.Request objects for each URL in the
    start_urls attribute of the Spider, and assigns them the parse method
    of the spider as their callback function.
    """
        item = Product()
        j = response.xpath('.//*[@id="container"]/section/script[3]').xpath('./text()').extract_first().replace("$.TYSetProductDetail(","").replace(");","").replace('$.TYPageName = "urundetay";','').strip()
        _json = PrepareJSONDoubleQuoteProblem(j)
        _price =json.loads(response.xpath('.//*[@id="container"]/script[3]/text()').extract_first())
        self.log(_price)

        _p = Price()
        _p["Currency"]= _price["offers"]["priceCurrency"]
        _p["PriceWithDiscount"] = _json["SalePrice"]
        sizes = []
        for size in _json["AvaliableSize"].split('|'):
            s = Size()
            s["SizeName"]=size.split('_')[0]
            s["SizeStock"]=int(size.split('_')[1])
            sizes.append(s)

        item["Code"] = _price["mpn"]
        item["BrandName"] = _json["BrandName"]
        item["Name"] = _json["ProductName"]

        pics = []
        for pic in response.css('#thumbnailContainer li img').extract():
            soup = BeautifulSoup(pic, "lxml")
            p=Picture()
            p["PictureName"]=soup.find('img')["title"]
            p["PicturePath"]=soup.find('img')['data-zoom-image']
            pics.append(p)
 
        sCategory = []
        for subCategory in _json["CategoryHierarchy"].split('/'):
            b = BreadCrumbCategory()
            b["Name"]= subCategory
            sCategory.append(b)

        item['Size']= sizes
        item['Picture'] = pics
        item['Category'] = sCategory
        item["Additional"] = _json
        item["Price"] = _p
        item["url"] = response.url
        item["SiteName"] = "TrendyolGiyim"
        item["Desc"]=  response.css('.return-info-list').extract_first()
        yield item
      
 

 