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
    PictureName = Field()

class Size(Item):
    SizeName = Field()
    SizeStock = Field()

class VariantColors(Item):
    Color= Field()
    Product= Field()
    IconPicture= Field()
    url = Field();

class Product(Item):
    _id = Field()
    Name= Field()
    BrandName= Field()
    Code= Field()
    Desc= Field()
    ShippingDate= Field()
    Color= Field()
    url = Field()
    Size = Field()
    Picture = Field()
    Category = Field()
    SiteName = Field()
    Price = Field()
    LinkedProduct = Field()
    Additional = Field()

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
