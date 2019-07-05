import re
import urllib.request
from urllib import parse

f = open('modle_data.json','r')
data = f.read()

all = re.findall(r'{.*?}', data,re.S)[0:20]
all_1 = urllib.parse.urlencode(all).encode('utf-8')

with open('clear_data.txt','w') as w:
    w.write(str(all_1))
