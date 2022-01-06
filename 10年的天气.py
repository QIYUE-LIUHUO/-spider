# 用于爬取信息
import requests
# 用于解析网页
from bs4 import BeautifulSoup
# 用于正则匹配找到目标项目
import re
# 对csv文件的操作
import csv
# 作图工具
from matplotlib import pyplot as plt
import time
import os
import openpyxl

# wb = openpyxl.load_workbook(r'F:\\爬虫\\期末作业\\天气.xlsx')
# ws = wb["sheet1"]
# name = ws.value
# for cell in name:
#     wb.create_sheet(title=str(cell[0]))
# wb.save(r'F:\\爬虫\\期末作业\\天气.xlsx')


# UA伪装
name = input("请输入你要访问的信息:")
name1 = input("再输一遍中文吗？")
param = {
    'query': name
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53'
}

# 打开文件
# a+权限追加写入
# newline=""用于取消自动换行
fp = open(name1+"天气预报.csv", "a+", newline="")
# 修饰，处理成支持scv读取的文件
csv_fp = csv.writer(fp)
# 设置csv文件内标题头
head = ['日期地区', '什么雨', '最高气温', '最低气温', '什么风', '什么风']
# 写入标题
csv_fp.writerow(head)


# 存放全部数据
data = []
# url1 ="http://www.tianqihoubao.com/lishi/"+name+ "/month/"
# 进行url拼接，主要拼接的是年份和月份
# 从2011年到2022
for i in range(2011, 2021):
    # 从1月到12月
    for j in range(1, 13):
        # 字符串化,方式吧20xx年弄成2，0，x，x
        i = str(i)
        # 小于10则补0
        if j < 10:  # 09月
            j = "0" + str(j)
        else:
            # 字符串化
            j = str(j)
        # 完成拼接
        url = "http://www.tianqihoubao.com/lishi/"+name+"/month/" + i + j + ".html"

        # 获取响应
        response = requests.get(url=url, headers=headers)
        # 设置编码为gbk
        response.encoding = 'gbk'
        # 获取响应文本数据
        page = response.text
        # 用BeautifulSoup解析网页
        soup = BeautifulSoup(page, 'lxml')
        # 获取所有tr标签
        tr_list = soup.find_all('tr')

        # 解析每一个tr标签
        for tr in tr_list:
            # 用于存放一天的数据
            one_day = []
            # 字符串化便于正则匹配
            tr = str(tr)
            # 去除所有空格
            tr = tr.replace(" ", "")
            # 取出日期
            date = re.findall(r'title="(.*?)'+name1+'天气预报">', tr)
            # 如果取到则放入one——day存放
            if date:
                one_day.append(date[0])
            # 取出风向
            date = re.findall(r'(.*?)雨', tr)
            # 如果取到则放入one——day存放
            if date:
                one_day.append(date[0])
            # 取出最高温和最低温
            tem = re.findall(r'(.*?)℃', tr)
            # 如果取到则放入one——day存放
            if tem:
                one_day.append(tem[0])
                one_day.append(tem[1])
            # 取出风向
            tem = re.findall(r'(.*?)风', tr)
            # 如果取到则放入one——day存放
            if tem:
                one_day.append(tem[0])
                one_day.append(tem[1])
            # 如果完整的取到一天的数据则放入data存放
            if len(one_day) == 6:
                data.append(one_day)
                print(one_day)
                # 写入csv文件
                csv_fp.writerow(one_day)

            time.sleep(2)



# 关闭文件指针
fp.close()

# 存放日期
x = []
# 存放雨
w = []
# 存放最高气温
h = []
# 存放最低气温
l = []
# 存放风向
c = []
# 读取之前爬取的数据
with open(name1+"天气预报.csv") as f:
    reader = csv.reader(f)
    j = 1
    for i, rows in enumerate(reader):
        try:
            # 不要标题那一行
            if i:
                row = rows
                print(row)
                x.append(rows[0])
                w.append(row[1])
                h.append(int(rows[2]))
                l.append(int(rows[3]))
                c.append(rows[4])
        except:
            print("错啦错啦")
# 设置画板大小
fig = plt.figure(dpi=128, figsize=(20, 6))
# 显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 画最高气温
plt.plot(x, h, c="red", alpha=0.5)
# 画最低气温
plt.plot(x, l, c="blue", alpha=0.5)
# 区间渲染
plt.fill_between(x, h, l, facecolor="blue", alpha=0.2)
# 标题
plt.title(name+"市过去3658天的气温变化")
# y轴名称
plt.ylabel("气温")
# x轴名称
plt.xlabel("日期")
plt.xticks(x[::300])
plt.show()

