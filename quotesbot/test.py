import scrapy
import yaml

 
x = "{title: 'Erkek Lacivert  Günlük Ayakkabı',            description: '<ul><li>Materyal: Keten</li><li>İç Materyal: Keten</li><li>Taban: Kauçuk Taban</li></ul>',            url: '/erkek-lacivert-gunluk-ayakkabi-2538304',            code: 'C-73994',            id: '2538304',            price: '109.99',            old_price: '189.99',            images: ['http:as']              }"
print(yaml.load(x))
