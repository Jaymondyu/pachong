import re


f = open('modle_data.json','r',encoding='utf-8')
data = f.read()

bottom = re.findall(r'底部高程\\",\\"attrValue\\":\\"(.*?)\\",\\"category\\":\\"尺寸标注\\',data,re.S)
top = re.findall(r'顶部高程\\",\\"attrValue\\":\\"(.*?)\\",\\"category\\":\\"尺寸标注\\',data,re.S)
id = re.findall(r'"description\\":\\"system\\",\\"entityId\\":\\"(.*?)\\",\\"id\\":\\"',data,re.S)

print(bottom)
print(top)
print(id)
