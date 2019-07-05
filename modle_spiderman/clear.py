import re

f = file.open('modle_data.txt')
data = f.read()

all = re.findall(r'{.*?}', data,re.S)[0]

print(all)
