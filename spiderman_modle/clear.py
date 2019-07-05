import re
import urllib.request
from urllib import parse

f = open('modle_data.json','r',encoding='utf-8')
data = f.read()

all = re.findall(r'{.*?}', data,re.S)


with open('clear_data.txt','w',encoding='utf-8') as w:
    w.write(str(all))
