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
from quotesbot.Tools  import StringToFloat

class MorHipoProductListPage(CrawlSpider):
    name = "MorhipoProductListPage"
    allowed_domains = ['www.morhipo.com', ]
    start_urls = [
        'https://www.morhipo.com/spor-giyim-erkek-ayakkabi/577/liste',]
 
        

    rules = (
        # find next page  liste?ps=120&pg=2
        Rule(
            LinkExtractor(
                allow=(r'ps=\d+&pg=\d+', ),
                restrict_css=('.bottom-pager.numarator', ),
                unique=True,
            ),
            
            follow=True,
        ),
        # go detail page
        Rule(
            LinkExtractor(
                restrict_css=('#products li', ),
                unique=True,
            ),
            callback='parse_post_detail',
        ),
    )

    def parse_post_detail(self, response):
        item = Product()
        _p = Price()
        _pid=0
        for s in response.css("script::text").extract():
            if s.find("var product =") >0:
                _dict = yaml.load(s.replace("var product =","").replace(';',""))
                _pid=_dict["identifier"]
            elif s.find("fullDetailsForSk") >0:
                _json = json.loads(s.replace("var fullDetailsForSk= ","").replace(';',""))
                item["Name"] = _json["name"]
                item["Desc"]=response.css("#aboutprodtab div div").extract_first()
                item["url"] = _json["canonicalUrl"]
                item["BrandName"] = _json["brandName"]

                _p["PriceWithDiscount"] = StringToFloat(_json["salesPrice"].replace("TL",""))
                _p["Price"] = StringToFloat(_json["previousPrice"].replace("TL",""))
                _p["DiscountPerc"] = (_p["Price"]-_p["PriceWithDiscount"])*100/_p["Price"]

                sCategory = []
                _b = BreadCrumbCategory()
                _b["Name"]= _json["category"]
                sCategory.append(_b)

                _b = BreadCrumbCategory()
                _b["Name"]= _json["gender"]
                sCategory.append(_b)

                for subCategory in response.css(".breadcrumb li a").extract():
                    soup = BeautifulSoup(subCategory, "lxml")
                    subcat= soup.find('a').text
                    if subcat == "Anasayfa":
                        pass
                    elif subcat == item["Name"]:
                        pass
                    else:
                        b = BreadCrumbCategory()
                        b["Name"]= subcat
                        b["Url"]= soup.find('a')["href"]
                        sCategory.append(b)

                item['Category'] = sCategory

                pictures = []
                for i in response.css("#carousel ul li a").extract():
                    soup = BeautifulSoup(i, "lxml")
                    p=Picture()
                    p["PicturePath"]=soup.find('a')["href"]
                    p["PictureName"]=soup.find('img')["title"]
                    pictures.append(p)
                item['Picture']= pictures

                sizes = []
                for renk in _json["Colors"]:
                    for size in renk["AvailableSizes"]:
                        if size["ProductID"] == _pid:
                            item["Color"]=renk["Name"]

                for renk in _json["Colors"]:
                    if renk["Name"] == item["Color"]:
                        for size in renk["AvailableSizes"]:
                            s = Size()
                            s["SizeName"]=size["Name"]
                            sizes.append(s)
                item['Size']= sizes
                     
        item["Code"] = response.xpath('.//*[@id="aboutprodtab"]/div/div/p[1]/text()').extract_first()
        item["SiteName"] = "MorHipo"

        yield item
 

              
               
                
        
                

                

               

