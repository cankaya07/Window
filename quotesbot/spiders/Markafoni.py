from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
from bs4 import BeautifulSoup
from quotesbot.Classes import Size, Picture, BreadCrumbCategory, Price,VariantColors, Product
import inspect
from quotesbot.Tools import PrepareJSONDoubleQuoteProblem
import json
import yaml
 
 
 
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
        item = Product()
        _p = Price()

        for s in response.css("script::text").extract():
            if s.find("window.productInfo") >0:
                _dict = yaml.load(s.replace("window.productInfo =","").replace('"',"'"))
                item["Name"] = _dict["title"]
                item["Desc"]=_dict["description"]
                item["url"] = _dict["url"]
                
                
                _p["PriceWithDiscount"] = float(_dict["price"])
                _p["Price"] = float(_dict["old_price"])
                _p["DiscountPerc"] = (_p["Price"]-_p["PriceWithDiscount"])*100/_p["Price"]
                
                pictures = []
                for i in _dict["images"]:
                    p=Picture()
                    p["PicturePath"]=i
                    pictures.append(p)
                item['Picture']= pictures
                sizes = []
                for i in _dict["sizes"]:
                    s = Size()
                    s["SizeName"]=i
                    sizes.append(s)
                item['Size']= sizes
                variants=[]
                for i in _dict["colors"]:
                    if item["url"]!=i["seo"]:
                        v = VariantColors();
                        v["Color"]=i["color_name"]
                        v["url"]=i["seo"]
                        v["IconPicture"]=i["product_image"]
                        variants.append(v)
                    elif:
                        item["Color"] = i["color_name"]
                item["LinkedProduct"]=variants
            elif s.find('GTMPush({"ecommerce"')>0:
                j = json.loads(s[s.index('GTMPush({"ecommerce"'):].replace('GTMPush(',"").replace(');',""))
                _p["Currency"]= j["ecommerce"]["currencyCode"]
                item["BrandName"] = j["ecommerce"]["detail"]["products"][0]["brand"]
                sCategory = []
                for subCategory in j["ecommerce"]["detail"]["products"][0]["category"].split('/'):
                    _b = BreadCrumbCategory()
                    _b["Name"]= subCategory
                    sCategory.append(_b)
                item['Category'] = sCategory








        item["Price"] = _p
        item["Code"] = response.css(".pro-product-add-button-wrapper button").xpath("./@data-product-no").extract_first()
        item["SiteName"] = "Markafoni"

        yield item
 