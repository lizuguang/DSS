import numpy as np
import matplotlib.pyplot as plt
import xlrd
def figure():
    fig, ax = plt.subplots(figsize=(7, 5))
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 13,
             }
    ax.tick_params(labelsize=12)
    # -------------两种算法能够支持的用户比例----------------------------------
    ax.set_ylabel(r'Block generation latency (s)', font1)
    x = np.arange(1, len(transaction_completion_time1) + 1, 1)
    # ax.set_title('The bandwidth demand')
    ax.set_xlabel(r'Sequence number of submission', font1)
    marker = [".", "^", "x", "P"]
    ls = ["--", "-.", ":", "-"]
    # plt.savefig('fix.eps', dpi=300)  # 指定分辨率保存
    lns = ax.plot(x, transaction_completion_time1,  marker = "v", ls = "-", color="deepskyblue", label= r"16 operators")
    #lns2 = ax.plot(x, transaction_completion_time2, marker = marker[0], ls = ls[0], label= r"4 Organization")
    lns3 = ax.plot(x, transaction_completion_time3, marker = marker[0], ls = ls[0], color="orangered", label= r"32 operators")
    lns =  lns + lns3
    labs = [l.get_label() for l in lns]
    ax.set_ylim(0, 250, 40)
    x_ticks = np.arange(0, len(transaction_completion_time1) + 1, len(transaction_completion_time1) / 5)
    plt.xticks(x_ticks)
    ax.legend(lns, labs, loc = 1, prop=font2, framealpha=0.8)
    ax.grid()
    #ax.margins(0)
    plt.savefig('E:\cloud files\Students\lizuguang\my papers\preparing\IEEEtran\Figure\\latency_s2.eps', dpi=600)
    plt.show()
# 读取excel表格
def readexcel(path, column):
    # 读取excel表格
    wb = xlrd.open_workbook(path)  # 打开Excel文件
    sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表
    R = []  # 创建空list
    for a in range(1, sheet.nrows, 1):  # 循环读取表格内容（每次读取一行数据），第一行为无用数据，不读
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        R.append(float(cells[column]))  # 把每次循环读取的数据插入到R
    return R
path1 = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\仿真3\\3组织_hash_100组数据.xls"
#path2 = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\仿真3\\3组织_100组数据.xls"
path3 = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\仿真3\\5组织_hash_100组数据.xls"
transaction_completion_time1 = readexcel(path1, 4)
#transaction_completion_time2 = readexcel(path2, 4)
transaction_completion_time3 = readexcel(path3, 4)
leng = len(transaction_completion_time1)
for i in range(50):
    a1 = transaction_completion_time1[i]
    a3 = transaction_completion_time3[i]
    transaction_completion_time1[i] = transaction_completion_time1[leng - 1 - i]
    transaction_completion_time1[leng - 1 - i] = a1
    transaction_completion_time3[i] = transaction_completion_time3[leng - 1 - i]
    transaction_completion_time3[leng - 1 - i] = a3
figure()
