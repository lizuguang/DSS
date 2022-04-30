import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
from matplotlib.pyplot import MultipleLocator
# 设置字体
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 18,
         }
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 15,
         }
def boxplot(y):
    plt.figure(figsize=(8, 6))
    labels = '8', '16', '24', '32'
    plt.boxplot(y, labels = labels, showfliers = True, patch_artist = True, widths = 0.4, boxprops ={'color':'black', 'facecolor':'lightgreen'}, medianprops = {'color':'black', 'linewidth': 1.8})  # 也可用plot.box()
    plt.xlabel('Number of organizations', font1)
    plt.ylabel('Submission latency (s)', font1)
    #labels2 = ["Mean value", "Abnormal data"]
    #plt.legend(labels = labels2, prop = font2)
    plt.xticks(font = font2)
    plt.yticks(font = font2)
    plt.xlim((0.6, 4.7))
    #plt.xlim(0, 32, 8)
    #plt.xticks(np.arange(0, 5, 1))
    plt.savefig('submission_latency.jpg', dpi=300)
    plt.show()
# 读取excel表格
def readexcel(filename):
    # 读取excel表格
    wb = xlrd.open_workbook("E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\仿真1\\20次迭代\\" + filename)  # 打开Excel文件
    sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表
    R = []  # 创建空list
    for a in range(1, sheet.nrows, 1):  # 循环读取表格内容（每次读取一行数据），第一行为无用数据，不读
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        R.append(cells[3])  # 把每次循环读取的数据插入到R
    return R
#计算中位数
def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2
num_peer = 4
time_peers_list = np.empty(shape=(50, num_peer))
for i in range(0, num_peer):
    data_peers = readexcel(str(i*8 + 8) + "peers.xls")
    time_peers_list[:, i] = data_peers
    print(get_median(data_peers))
boxplot(time_peers_list)

