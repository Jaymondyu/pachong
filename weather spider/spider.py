#coding:utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(url):
    # url="http://www.tianqihoubao.com/weather/top/jiangjin.html"

    response = requests.get(url)

    html = response.content.decode('GB2312')

    # 提取数据(简单的语法)
    # soup会自动整理已有的数据
    soup = BeautifulSoup(html,'html.parser')

    tr_list = soup.find_all('tr')

    # 对数据进行格式化

    dates,conditions,temps=[],[],[]

    for data in tr_list[1:]:
        sub_data = data.text.split()
        dates.append(sub_data[0])
        conditions.append(''.join(sub_data[1:3]))
        temps.append(''.join(sub_data[3:6]))

# 用 pd.DataFrame() 讲整理好的格式化数据 放入表格中
    _data = pd.DataFrame()
    _data['日期'] = dates
    _data['天气'] = conditions
    _data['温度'] = temps

    return _data


data_1_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201901.html')
data_2_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201902.html')
data_3_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201903.html')
data_4_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201904.html')
data_5_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201905.html')
data_6_mouth = get_data('http://www.tianqihoubao.com/lishi/jiangjin/month/201906.html')



# 将几个表格进行上下拼接
data = pd.concat([data_1_mouth,data_2_mouth,data_3_mouth,data_4_mouth,data_5_mouth,data_6_mouth]).reset_index(drop=True)

#保存数据
data.to_csv('Jiangjin.csv',index=False,encoding='utf-8')