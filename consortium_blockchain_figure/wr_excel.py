import xlrd
import xlwt
# 读取excel表格
def readexcel(ID, type):
    # 读取excel表格
    wb = xlrd.open_workbook("E:\\pycharmprojects\\pythonProject1\\TOF" + type + "数据\\TOF数据" + str(ID) + '.' + type + '.xls')  # 打开Excel文件
    sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表
    R = []  # 创建空list
    for a in range(1, sheet.nrows, 1):  # 循环读取表格内容（每次读取一行数据），第一行为无用数据，不读
        cells = sheet.row_values(a)  # 每行数据赋值给cells
        R.append(cells[1:5])  # 把每次循环读取的数据插入到R
    return R
# 写excel文件
def w_excel1(system_time, response_list):
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("Sheet1", cell_overwrite_ok=True)  # 新建sheet
    # ---设置居中对齐和字体----
    style1 = xlwt.XFStyle()
    style2 = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style1.alignment = al
    style2.alignment = al
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    style1.font = font
    # ------------------------
    sheet1.write(0, 0, "序号", style1)
    sheet1.write(0, 1, "Responses内容", style1)
    sheet1.write(0, 2, "完成一次区块上传的耗时", style1)
    filename = "E:\\cloud files\\Students\\lizuguang\\my papers\\preparing\\Simulation\\consortium_blockchain\\上传耗时.xls"
    num = len(system_time)
    for i in range(num):
        sheet1.write(i + 1, 0, i + 1, style2)
        sheet1.write(i + 1, 1, response_list[i], style2)
        sheet1.write(i + 1, 2, system_time[i], style2)
    # 设置列宽
    for n in range(3):
        first_col = sheet1.col(n)
        first_col.width = 256 * 30
    workbook.save(filename)  # 保存

# 写excel文件
def w_excel2(response_list, EndTime_list, Time_list, num):
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("Sheet1", cell_overwrite_ok=True)  # 新建sheet
    # ---设置居中对齐和字体----
    style1 = xlwt.XFStyle()
    style2 = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style1.alignment = al
    style2.alignment = al
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    style1.font = font
    # ------------------------
    sheet1.write(0, 0, "序号", style1)
    sheet1.write(0, 1, "Responses内容", style1)
    sheet1.write(0, 2, "完成提交的时间点", style1)
    sheet1.write(0, 3, "计算交易策略+提交策略的平均延时", style1)
    filename = "E:\cloud files\\Students\\lizuguang\\my papers\\preparing\\Simulation\\results\\仿真1\\20次迭代\\" + str(num * 2) + "peers.xls"
    num = len(Time_list)
    for i in range(num):
        sheet1.write(i + 1, 0, i + 1, style2)
        sheet1.write(i + 1, 1, response_list[i], style2)
        sheet1.write(i + 1, 2, EndTime_list[i], style2)
        sheet1.write(i + 1, 3, Time_list[i], style2)
    # 设置列宽
    for n in range(4):
        first_col = sheet1.col(n)
        first_col.width = 256 * 30
    workbook.save(filename)  # 保存
# 写excel文件
def w_excel3(blockHash_list, createTimestamp_list, updatedAt_list, transaction_completion_time_list):
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("Sheet1", cell_overwrite_ok=True)  # 新建sheet
    # ---设置居中对齐和字体----
    style1 = xlwt.XFStyle()
    style2 = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style1.alignment = al
    style2.alignment = al
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    style1.font = font
    # ------------------------
    sheet1.write(0, 0, "序号", style1)
    sheet1.write(0, 1, "blockHash", style1)
    sheet1.write(0, 2, "createTimestamp", style1)
    sheet1.write(0, 3, "updatedAt", style1)
    sheet1.write(0, 4, "transaction_completion_time", style1)
    filename = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\\results\仿真3\\5组织_hash_100组数据.xls"
    num = len(blockHash_list)
    for i in range(num):
        sheet1.write(i + 1, 0, i + 1, style2)
        sheet1.write(i + 1, 1, blockHash_list[i], style2)
        sheet1.write(i + 1, 2, createTimestamp_list[i], style2)
        sheet1.write(i + 1, 3, updatedAt_list[i], style2)
        sheet1.write(i + 1, 4, transaction_completion_time_list[i], style2)
    # 设置列宽
    for n in range(5):
        first_col = sheet1.col(n)
        first_col.width = 256 * 30
    workbook.save(filename)  # 保存