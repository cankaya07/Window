from Tools import PrepareJSONDoubleQuoteProblem
import json
import re


x ='{\r\n            ProductId: 51942798,\r\n            BoutiqueId: 188033,\r\n            ProductCategoryGroupId: 870,\r\n            ProductGenderType: \'Erkek\',\r\n            BoutiqueName: \'Soho Exclusive &amp; Soho Men : Yeni Ürünlerle\',\r\n            BoutiqueNameSeo: \'Soho-Exclusive--Soho-Men---Yeni-urunlerle\',\r\n            ProductName: \'Siyah Erkek Sneaker\',\r\n            ProductNameSeo: \'Siyah-Erkek-Sneaker\',\r\n            ProductCategoryName: \'Sneaker\',\r\n            ProductCategoryNameReport: \'Sneaker\',\r\n            SalePrice:79.99,\r\n            SelectedVariant:{text:\'\', value: \'\'},\r\n            SelectedGenderTypeName: \'\',\r\n            ProductStatu:\'Available\',\r\n            ProductMainId:\'3754453\',\r\n            ColorId: \'2\',\r\n            Color: \'2_SIYAH\',\r\n            ProductColor:\'2_SIYAH\',\r\n            BusinessUnit :\'Branded Shoes B\',\r\n            TaxRate :8,\r\n            BoutiqueCloseDate: "2018-06-25T05:45:00",\r\n            BoutiqueStartDate: "2018-06-22T06:00:00",\r\n            Margin :\'5\',\r\n            Sku :\'BB00023896\',\r\n            FastDelivery :\'1\',\r\n            BrandName: "Soho-Men",\r\n            Barcode:"Soho-Men",\r\n            BoutiqueStatus: "Open",\r\n            ProductMerchant: "TRENDYOL",\r\n            IsRushDeliveryTimeEnable: "True",\r\n            AvaliableSize: "40_1|41_1|42_1|43_1|44_1",\r\n            ProductContentId: "2153661",\r\n            CategoryHierarchy: "Ayakkabı/Spor Ayakkabı/Sneaker"\r\n        }'
 


PrepareJSONDoubleQuoteProblem(x)




 