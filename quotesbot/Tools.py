# 1.184,00 
# 984,00
def StringToFloat(str):
    return float(str.replace(".","").replace(",","."))

def PrepareJSONDoubleQuoteProblem(str):
    import re
    import json

    regex = re.compile('(\'.*\',)')
    str = regex.sub(lambda m: m.group().replace(':'," ",1), str)
    str = str.replace("'",'"')
    
    pattern = re.compile(r'(\w+\s{0,10}?[^0-9]):')
    response = pattern.sub(r'"\1": ', str)
    j = json
    try:
        j= json.loads(response)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
        print(response)

    return j