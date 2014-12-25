#-*- coding:utf-8 -*    
import os
from openpyxl.reader.excel import load_workbook  
import sqlite3
import  time  

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('e:/working/transdb/trans.db')
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    sqlite_db = connect_db()
    return sqlite_db

def read_excel_file(filename, db):

	#开始时间
	startTime = time.time()  

	#读取excel2007文件  
	wb = load_workbook(filename = r'static/Uploads/'+filename)  

	#显示有多少张表  
	ranges = wb.get_named_ranges()  

	#取第一张表  
	sheetnames = wb.get_sheet_names()  
	ws = wb.get_sheet_by_name(sheetnames[0])  

	#显示表名，表行数，表列数  
	title = ws.title  
	row = ws.get_highest_row()  
	colum = ws.get_highest_column()  

	# 建立存储数据的字典   
	data_dic = {}   

	#把数据存到字典中  
	for rx in range(ws.get_highest_row()):  

		temp_list = []  
		w1 = ws.cell(row = rx+2,column = 1).value  
		w2 = ws.cell(row = rx+2,column = 2).value  
		w3 = ws.cell(row = rx+2,column = 3).value  
		temp_list = [w1,w2,w3]
		data_dic[rx] = temp_list
		if w1 == 'break':
			break

		cur = db.execute('select area, chinese, english from translations where area=? AND chinese=? AND english=?',[w1,w2,w3])
		entries = cur.fetchall()
		if not entries:
			db.execute('insert into translations (area, chinese, english) values (?, ?, ?)', [w1,w2,w3])

	db.commit()
		
	w1 = ws.cell(row = 2,column = 1).value  
	return 'Total:%d' %rx
