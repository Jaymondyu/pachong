import urllib.request
import urllib.parse
import string

url = 'https://www.ucl.ac.uk/maini-group/team/currentmembers'

headers = {
    "User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}


request = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(url)

data = response.read().decode("utf-8")


with open("ucl.html", "w", encoding='utf-8')as f:
    f.write(data)