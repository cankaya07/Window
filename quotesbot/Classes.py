import scrapy

class WebSite(scrapy.Item):
    SiteName = scrapy.Field()
    HomePageUrl = scrapy.Field()

class Price(scrapy.Item):
    Price= scrapy.Field()
    PriceWithDiscount= scrapy.Field()
    DiscountPerc= scrapy.Field()
    Currency= scrapy.Field()
    FreightAmount= scrapy.Field()

class Picture(scrapy.Item):
    PicturePath = scrapy.Field()

class Size(scrapy.Item):
    SizeName = scrapy.Field()
    SizeStock = scrapy.Field()

class VariantColors(scrapy.Item):
    Color= scrapy.Field()
    Product= scrapy.Field()
    IconPicture= scrapy.Field()

class Product(scrapy.Item):
    Name= scrapy.Field()
    BrandName= scrapy.Field()
    Code= scrapy.Field()
    Desc= scrapy.Field()
    ShippingDate= scrapy.Field()
    Color= scrapy.Field()
 
    last_updated = scrapy.Field(serializer=str)

class Model(scrapy.Item):
    Height= scrapy.Field()
    Weight= scrapy.Field()
    Chest= scrapy.Field()
    Waist= scrapy.Field()
    Hipline= scrapy.Field()
    Bodysize= scrapy.Field()

class BreadCrumbCategory(scrapy.Item):
    Name = scrapy.Field()
    Url = scrapy.Field()
