import xlrd
from datetime import datetime
# 读取excel表格
def readexcel(path, column):
    # 读取excel表格
    wb = xlrd.open_workbook(path)  # 打开Excel文件
    sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表
    R = []  # 创建空list
    for a in range(1, sheet.nrows, 1):  # 循环读取表格内容（每次读取一行数据），第一行为无用数据，不读
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        R.append(cells[column])  # 把每次循环读取的数据插入到R
    return R
def calculate_time(timestamp_list1, timestamp_list2):
    blockbroadcated_time = []
    leng = len(timestamp_list1)
    for i in range(leng):
        str_time = datetime.strptime(timestamp_list1[i], '%Y-%m-%d %H:%M:%S.%f')
        str_time2 = datetime.strptime(timestamp_list2[leng - i - 1], '%Y-%m-%d %H:%M:%S.%f')
        blockbroadcated_time.append((str_time2 - str_time).total_seconds())
    return blockbroadcated_time
if __name__ == '__main__':
    path1 = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\组织数为3\\blocksize=10\时间间隔为3\\3运营商_20次迭代_blocksize=10_仿真2).xls"
    # update_timestamp 为完成提交区块的时间戳
    update_timestamp = readexcel(path1, 2)
    # updateblock_time 为计算交易策略+提交策略的平均时延
    updateblock_time = readexcel(path1, 3)
    path2 = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\组织数为3\\blocksize=10\时间间隔为3\\3运营商_20次迭代_blocksize=10_仿真3).xls"
    # cratedblock_timestamp为区块生成的时间戳
    cratedblock_timestamp = readexcel(path2, 1)
    blockbroadcated_time = calculate_time(update_timestamp, cratedblock_timestamp)
    print(blockbroadcated_time)
