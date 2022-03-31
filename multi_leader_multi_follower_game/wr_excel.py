import xlrd
import xlwt
# 写excel文件
def w_excel1(U_N_dynamic, U_N_fixed):
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
    sheet1.write(0, 0, "U_N2_dynamic", style1)
    sheet1.write(0, 1, "U_N2_fixed", style1)
    sheet1.write(0, 2, "U_N4_dynamic", style1)
    sheet1.write(0, 3, "U_N4_fixed", style1)
    filename = "E:\cloud files\Students\lizuguang\my papers\preparing\Simulation\multi_leader_multi_follower_game\\fixed_price.xls"
    num = len(U_N_dynamic[:, 0])
    for i in range(num):
        sheet1.write(i + 1, 0, U_N_dynamic[i][0], style2)
        sheet1.write(i + 1, 1, U_N_fixed[i][0], style2)
        sheet1.write(i + 1, 2, U_N_dynamic[i][1], style2)
        sheet1.write(i + 1, 3, U_N_fixed[i][1], style2)
    # 设置列宽
    for n in range(3):
        first_col = sheet1.col(n)
        first_col.width = 256 * 30
    workbook.save(filename)  # 保存