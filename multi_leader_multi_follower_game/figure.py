import xlrd
import xlwt
import matplotlib.pyplot as plt
import numpy as np
def figure():
    fig, ax = plt.subplots()
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 13,
             }
    ax.tick_params(labelsize=13)
    # -------------两种算法能够支持的用户比例----------------------------------
    ax.set_ylabel(r'Utility of provider', font1)
    x = np.arange(0, cycle_index * m * l_m_lag, l_m_lag * m)
    # ax.set_title('The bandwidth demand')
    ax.set_xlabel(r'Total budgets of requestors', font1)
    marker = [".", "^", "P", "x"]
    ls = ["-", "-.", ":", "-."]
    color = ["blue", "dodgerblue", "crimson","indianred"]
    linewidth = 1.6
    # plt.savefig('fix.eps', dpi=300)  # 指定分辨率保存
    lns1 = ax.plot(x, R[:, 0],  marker = marker[2], ls = ls[0], color= color[0], linewidth = linewidth, label= r"Provider 2 with dynamic price")
    lns2 = ax.plot(x, R[:, 1], marker= marker[2], ls= ls[2], color = color[0], linewidth = linewidth, label=r"Provider 2 with fixed price")
    lns3 = ax.plot(x, R[:, 2], marker = marker[1], ls = ls[0], color = color[2], linewidth = linewidth, label= "Provider 4 with dynamic price")
    lns4 = ax.plot(x, R[:, 3], marker=marker[1], ls=ls[2], color = color[2], linewidth = linewidth, label="Provider 4 with fixed price")
    lns = lns1 + lns2 + lns3 + lns4
    labs = [l.get_label() for l in lns]
    ax.set_ylim(0, 200, 40)
    x_ticks = np.arange(0, cycle_index * m * l_m_lag, l_m_lag * m * 4)
    plt.xticks(x_ticks)
    ax.legend(lns, labs, loc = 2, prop=font2, framealpha=0.5)
    ax.grid()
    ax.margins(0)
    plt.savefig('fixed_price.eps', dpi=300)
    plt.show()
# 读取excel表格
def readexcel():
    # 读取excel表格
    wb = xlrd.open_workbook("E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\multi_leader_multi_follower_game\\fixed_price.xls")  # 打开Excel文件
    sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表
    R = np.zeros([cycle_index, 4])  # 创建空list
    for a in range(1, sheet.nrows, 1):  # 循环读取表格内容（每次读取一行数据），第一行为无用数据，不读
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        R[a-1, :] = cells  # 把每次循环读取的数据插入到R
    return R
cycle_index = 21
l_m_lag = 2
m = 50
R = readexcel()
figure()