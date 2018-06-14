from scrapy.item import Item, Field


class WebSite(Item):
    SiteName = Field()
    HomePageUrl = Field()

class Price(Item):
    Price= Field()
    PriceWithDiscount= Field()
    DiscountPerc= Field()
    Currency= Field()
    FreightAmount= Field()

class Picture(Item):
    PicturePath = Field()

class Size(Item):
    SizeName = Field()
    SizeStock = Field()

class VariantColors(Item):
    Color= Field()
    Product= Field()
    IconPicture= Field()

class Product(Item):
    Name= Field()
    BrandName= Field()
    Code= Field()
    Desc= Field()
    ShippingDate= Field()
    Color= Field()
    Url = Field()
 
    last_updated = scrapy.Field(serializer=str)

class Model(Item):
    Height= Field()
    Weight= Field()
    Chest= Field()
    Waist= Field()
    Hipline= Field()
    Bodysize= Field()

class BreadCrumbCategory(Item):
    Name = Field()
    Url = Field()
