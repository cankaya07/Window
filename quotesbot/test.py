from pymongo import MongoClient
import json
from Classes import Product

client = MongoClient()
client = MongoClient('mongodb://localhost:27017')
db = client['Vitrin']
collection = db['Sites']
p = Product()
obj = collection.find_one({"url": '/new-balance-evergreen-1'})
p= obj
p['Name']='New Balance 574 Evergreen'

print(p)
 
collection.update({'url': p['url']}, dict(p), upsert=True)




 