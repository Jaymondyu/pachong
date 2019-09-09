# coding:utf-8
#
# https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=%E5%8D%B0%E7%AC%AC%E5%AE%89%E8%80%81%E6%96%91%E9%B8%A0

# https://y.qq.com/n/yqq/song/002GQJAQ3w9yuh.html


from selenium import webdriver
import requests
import json
import re
import urllib



Chrome_driver = "C:\Users\Administrator\Desktop\chromedriver.exe"

name = raw_input("输入歌曲名:")
driver = webdriver.Chrome(executable_path=Chrome_driver)
url = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}".format(name)

def get_url():
    driver.get(url)
    driver.implicitly_wait(5)
    data = driver.find_element_by_xpath('//*[@id="song_box"]/div[2]/ul[2]/li[1]/div/div[2]/span/a').get_attribute("href")
    data = {"mid":data}
    return data

def get_music(data):
    url = "http://www.douqq.com/qqmusic/qqapi.php"
    req = requests.post(url,data=data).text
    req = json.loads(req)
    req = req.replace ('\/\/','//').replace('\/','/')
    rg = re.compile('"mp3_1":"(.*?)",')
    rs = re.findall(rg,req)
    print(rs)
    return rs





def run():
    data = get_url()
    rs = get_music(data)
    requests.get(rs)
run()

