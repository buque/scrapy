# -*- coding: utf-8 -*-
"""
存储数据
"""
import itertools
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
from queue import Queue
import time


class MyIO():
    def __init__(self, fileName):
        self.fileName = fileName
        self.cnt = 0
    
    def openFile(self):
        workbook = open_workbook(self.fileName)

        #当前写索引
        self.rows = workbook.sheets()[0].nrows
        self.excel = copy(workbook) 
        
        #当前sheet页
        self.table = self.excel.get_sheet(0)
        return True

    def putData(self, data):
        '''Write data to txt.'''
        try:
            self.openFile()
            for (k,v) in data.items():
                i = 0
                for value in v:
                    self.table.write(self.rows, i, value[1])
                    i = i+1
                self.rows = self.rows+1
            self.excel.save(self.fileName)
        except:
            print("There are a error!")
        else:
            print('Write times: ', self.rows)
            self.cnt = self.cnt + 1
        return

        # workbook = xlwt.Workbook(encoding='utf-8')
        # sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        # sheet.write(0, 0, line[0])
        # sheet.write(0, 1, line[1])
        # sheet.write(0, 2, line[2])
        # sheet.write(0, 3, line[3])
        
        # for content in data:
        #     sheet.write(i, 0, content[0], datastyle)
        #     for j in range(1, 4):
        #         sheet.write(i, j, content[j])
        #     i = i + 1
        # workbook.save(self.fileName)
