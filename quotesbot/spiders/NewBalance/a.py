# -*- coding: utf-8 -*-
import json



class asda():
    with open('NBMainCategories.json') as json_data:
        d = json.load(json_data)
        print(type(d))

asda()