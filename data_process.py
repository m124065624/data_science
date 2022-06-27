# -*- coding: utf-8 -*-
import openpyxl


def process():
    # 得到文本数据
    # 打开工作簿
    wb = openpyxl.load_workbook('data/meta.xlsx')
    # 获取表单
    sh = wb['数据元整理']
    # 读取指定的单元格数据
    rows = sh.rows

    content = ""
    count = -1

    # 按列读取所有数据，每一列的单元格放入一个元组中
    for row in list(rows):  # 遍历每行数据
        count += 1
        for c in row:  # 把每行的每个单元格的值取出来，存放到case里
            if c.value and count > 0 and (c.value not in content):
                content += c.value + '\n'

    # 保存数据
    open('data/result.txt', 'w+', encoding='utf8').write(content)
