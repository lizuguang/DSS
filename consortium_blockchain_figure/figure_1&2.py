import numpy as np
import matplotlib.pyplot as plt

def figure_1():
    # 仿真1数据列
    six_peers = [5.83, 6.22, 6.93, 7.55]
    eleven_peers = [6.62, 7.79, 10.36, 13.9]
    sixteen_peers = [7.21, 10.81, 17.2, 28.96]
    shops = range(2, 6)
    # 创建分组柱状图，需要自己控制x轴坐标
    xticks = np.arange(len(shops))
    fig, ax = plt.subplots(1)
    #fig, ax = plt.subplots(figsize=(10, 7))
    # 所有门店第一种产品的销量，注意控制柱子的宽度，这里选择0.25
    ax.bar(xticks, six_peers, width=0.25, label="6 peers", color="red")
    # 所有门店第二种产品的销量，通过微调x轴坐标来调整新增柱子的位置
    ax.bar(xticks + 0.25, eleven_peers, width=0.25, label="11 peers", color="blue")
    # 所有门店第三种产品的销量，继续微调x轴坐标调整新增柱子的位置
    ax.bar(xticks + 0.5, sixteen_peers, width=0.25, label="16 peers", color="green")
    #ax.set_title("Grouped Bar plot", fontsize=15)
    ax.set_xlabel("Number of organizations", font1)
    ax.set_ylabel("Latency of calculating strategy (s)", font1)
    ax.legend(prop=font2)
    ax.grid()
    # 最后调整x轴标签的位置
    ax.set_xticks(xticks + 0.25)
    ax.set_xticklabels(shops)
    plt.show()
def figure_2():
    # 仿真2数据列
    ten_iterations = [5.76,	6.5, 7.78, 9.66]
    twenty_iterations = [6.62,7.79,10.36,13.9]
    thirty_iterations = [7.08,9.05,12.8,18.72]
    shops = range(2, 6)
    # 创建分组柱状图，需要自己控制x轴坐标
    xticks = np.arange(len(shops))
    fig, ax = plt.subplots()
    #fig, ax = plt.subplots(figsize=(10, 7))
    # 所有门店第一种产品的销量，注意控制柱子的宽度，这里选择0.25
    ax.bar(xticks, ten_iterations, width=0.25, label="10 iterations", color="red")
    # 所有门店第二种产品的销量，通过微调x轴坐标来调整新增柱子的位置
    ax.bar(xticks + 0.25, twenty_iterations, width=0.25, label="20 iterations", color="blue")
    # 所有门店第三种产品的销量，继续微调x轴坐标调整新增柱子的位置
    ax.bar(xticks + 0.5, thirty_iterations, width=0.25, label="30 iterations", color="green")
    #ax.set_title("Grouped Bar plot", fontsize=15)
    ax.set_ylim(0, 21, 5)
    ax.set_xlabel("Number of organizations", font1)
    ax.set_ylabel("Average latency (s)", font1)
    ax.legend(prop=font2)
    ax.grid()
    # 最后调整x轴标签的位置
    ax.set_xticks(xticks + 0.25)
    ax.set_xticklabels(shops)
    plt.show()
if __name__ == '__main__':
    # 设置字体
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 13,
             }
    figure_1()
    #figure_2()