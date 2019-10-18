import requests
import json
url = "https://www.mikecrm.com/handler/web/form_submit/handleGetListFormSubmitSummary.php"
headers = {
    "Cookie":"_ga=GA1.2.1156104193.1571202366; _gid=GA1.2.302567452.1571202366; PHPSESSID=2njniduju82dkra897549iag53; uvi=h1k2IPwJ1CwtuvKbdEtGOuVwtowMn5cj9rRdUmLg9zdno001; _gat=1; PHPSESSID=2njniduju82dkra897549iag53"
    }
data = {"d": (None,'{"cvs":{"i":200412098}}')}
respone = requests.post(url, headers=headers,files=data)
respone = json.loads(respone.content.decode('utf-8'))

info_list = []
n = 1
for i in respone["list"]["d"]:
    id = n
    name = i[4]["cp"]["204117630"]["n"]
    tel = i[4]["cp"]["204117633"][0]
    info = {"id":id,"name":name,"tel":tel}
    n=n+1
    info_list.append(info)

print (info_list)