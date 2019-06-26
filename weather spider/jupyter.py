#coding:utf-8
# 在 jupyter 中 运行
import pandas as pd
from matplotlib import pyplot as plt
#解决中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']
#解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False
# %matplotlib inline

#读取数据
#读取表格
data = pd.read_csv(r'C:\Users\YU\Desktop\GitHub\pachong\Jiangjin.csv')
#显示表头前几行
data.head(5)

#数据清洗
#检测缺失值
data.isnull()
#缺失值总览
(data.isnull()).sum()


#数据处理
#字符串处理
#数据分割
data['最高气温'] = data['温度'].str.split('/',expand=True)[0]
data['最低气温'] = data['温度'].str.split('/',expand=True)[1]
#更改数据类型(使用 lambda 函数，将 ℃ 符号删除了)
data['最高气温'] = data['最高气温'].map(lambda x:int(x.replace('℃','')))
data['最低气温'] = data['最低气温'].map(lambda x:int(x.replace('℃','')))


#绘图

dates=data['日期']
highs=data['最高气温']
lows=data['最低气温']


# 根据数据绘制图形
fig = plt.figure(dpi=128,figsize=(10,6))
plt.plot(dates,highs,c='red',alpha=0.5)
plt.plot(dates,lows,c='blue',alpha=0.5)

# 给图标区域着色
plt.fill_between(dates,highs,lows,facecolor='green',alpha=0.2)  # alpha值指定颜色的透明度(0为完全透明,1为完全不透明)

#设置图形格式
plt.title('2019江津天气', fontsize=24)  # 标题
plt.xlabel('日期',fontsize=12) # x轴标签
fig.autofmt_xdate() # 绘制斜的日期标签,以免重叠
plt.ylabel('温度',fontsize=12) # y轴标签

# 参数刻度线样式设置
plt.tick_params(axis='both',which='major',labelsize=10)

# 修改刻度
plt.xticks(dates[::10])

# 显示2019年每日最高气温折线图
plt.show()
