#-*- coding:utf-8 -*  
import sqlite3 
import time  
import sys  
#workbook相关  
from openpyxl.workbook import Workbook  
#万恶的ExcelWriter，妹的封装好了不早说，封装了很强大的excel写的功能  
from openpyxl.writer.excel import ExcelWriter  
#一个eggache的数字转为列字母的方法  
from openpyxl.cell import get_column_letter  
#新建一个workbook  
wb = Workbook()  
#新建一个excelWriter  
ew = ExcelWriter(workbook = wb)  
#设置文件输出路径与名称  
dest_filename = r'empty_book.xlsx'  
#第一个sheet是ws  
ws = wb.worksheets[0]  
#设置ws的名称  
ws.title = "range names"   
#录入数据，注意col是数字转字母，然后需要限定%s（string型）当参数传到ws.cell()方法中去,records可以想象为一个从数据库里查询出来的数据集合  
i=1  
table = {}  
records = {'sdfasdf','xxdfd','uiui','JJJ','sOPOPdf'}
for record in records:  
    for x in range(1,len(record)+1):  
        col = get_column_letter(x)  
        ws.cell('%s%s'%(col, i)).value = '%s' % (record[x-1])        
              
    i+=1  
#又建了一个sheet，ws名字都没变，太省了。。。但是确实是一个新的sheet，不会影响之前那个sheet的东西  
ws = wb.create_sheet()  
ws.title = 'Pi'  
ws.cell('F5').value = 3.14  
      
#写文件  
ew.save(filename = dest_filename)  