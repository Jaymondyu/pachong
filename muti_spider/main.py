# 多线程爬取猫眼电影数据

import requests
import parsel
import pprint

def get_info(page):
    # get方法请求数据
    response = requests.get('https://maoyan.com/board/4?offset={}'.format(page))

    # 提取数据方法 1.xpath  2.re正则表达式  3.css选择器


    sel = parsel.Selector(response.text)

    # 正则提取
    re = sel.re('<p class="releasetime">(.*?)</p>')
    # print(re)

    # xpath 提取
    xpath = sel.xpath('//p[@class="releasetime"]/text()').getall()
    # print(xpath)

    #css选择器 提取
    css_ = sel.css('p.releasetime::text').getall()
    # print(css_)


    # 使用css选择器 进行选择
    time = sel.css('p.releasetime::text').getall()
    star = sel.css('p.star::text').getall()
    name = sel.css('p.name a::text').getall()
    score = sel.css('p.score i::text').getall()

    # 使用 for循环 遍历<dd>中的内容
    dds = sel.css('dd')
    for dd in dds:
        # print(dd.css('p.name a::text').getall()[0].strip())
        # print(dd.css('p.star::text').getall()[0].strip())
        # print(dd.css('p.releasetime::text').getall()[0])
        # print(''.join(dd.css('p.score i::text').getall()))


        pprint.pprint({'电影名':dd.css('p.name a::text').getall()[0].strip(),
               '演员':dd.css('p.star::text').getall()[0].strip(),
               '发行时间':dd.css('p.releasetime::text').getall()[0],
               '评分': ''.join(dd.css('p.score i::text').getall())
               })
# 构造url 请求10页数据
for page in range(0,100,10):
    get_info(page)