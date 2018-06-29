from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
from bs4 import BeautifulSoup
from quotesbot.Classes import Size, Picture, BreadCrumbCategory, Price,VariantColors, Product
import inspect
from quotesbot.Tools import PrepareJSONDoubleQuoteProblem
import json
 
 
 
class MarkafoniProductListPage(CrawlSpider):
    name = "MarkafoniProductListPage"
    allowed_domains = ['www.markafoni.com', ]
    start_urls = [
        'https://www.markafoni.com/erkek-ayakkabi',]

    rules = (
        # find next page 
        Rule(
            LinkExtractor(
                allow=(r'\/?page=\d+', ),
                restrict_css=('.paginator', ),
                unique=True,
            ),
            follow=True,
        ),
        # go detail page 
        # //*[@id="pro-product-list-1910"]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div
        #//*[@id="pro-product-list-1910"]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div
        Rule(
            LinkExtractor(
                restrict_css=('.row.pro-product-list-items', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

  
   
 
    def parse_post_detail(self, response):
        self.log(response.url)
        startPointer= response.text.find("window.item_id")
         
      
 

 