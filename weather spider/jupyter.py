# 在 jupyter 中 运行
import pandas as pd

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
data['最高气温'] = data['气温'].str,split('/',expand=True)[0]
data['最低气温'] = data['气温'].str,split('/',expand=True)[1]
#更改数据类型(使用 lambda 函数，将 ℃ 符号删除了)
data['最高气温'] = data['最高气温'].map(lambda x:int(x.replace('℃','')))
data['最低气温'] = data['最低气温'].map(lambda x:int(x.replace('℃','')))


#绘图
