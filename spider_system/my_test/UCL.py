import urllib.request
import urllib.parse
import string

url = 'http://www.ucl.ac.uk/maini-group/team/currentmembers'

response = urllib.request.urlopen(url)

data = response.read().decode("utf-8")


with open("ucl.html", "w", encoding='utf-8')as f:
    f.write(data)