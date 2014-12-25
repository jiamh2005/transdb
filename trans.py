#-*- coding:utf-8 -*    
import os
from openpyxl.reader.excel import load_workbook  
import sqlite3
import time  

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename

import testread
from testread import read_excel_file

UPLOAD_FOLDER = 'static/Uploads'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'xlsx', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
   
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('trans.db')
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    sqlite_db = connect_db()
    return sqlite_db
  
@app.route('/import', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/readxls/'+filename)
            #return redirect(url_for('uploads',filename=filename),302)
            #return redirect('/uploads/'+filename)
    return render_template('import.html') 
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	

@app.route('/readxls/<filename>')
def readxls(filename):
	if filename.rsplit('.', 1)[1] == 'xlsx' :
		db = get_db()
		return read_excel_file(filename, db)
	return 'The file is not excel file!'

@app.route('/', methods=['GET', 'POST'])
def show_entries():
    db = get_db()
    substr = 'to'
    if request.method == 'POST':
        substr = request.form['search']
        substr ='%' + substr + '%'
        cur = db.execute('select id, area, chinese, english from translations where english like ? or chinese like ? order by english desc', [substr,substr])
        #cur = db.execute('select area, chinese, english from translations where english=? or chinese=? order by english desc', [substr,substr])
    else:
        cur = db.execute('select id, area, chinese, english from translations order by english desc')

    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        db = get_db()
        multirow = request.form['multirow']
        arr = multirow.split('\n')
        tresult = []
        for s1 in arr:
            ts = []
            s1 = s1.strip()
            ts.append(s1)
            cur = db.execute('select chinese, english from translations where english=? or chinese=?', [s1,s1])
            ens = cur.fetchall()
            if ens:
                if s1 == ens[0][0]:
                    ts.append(ens[0][1])
                else:
                    ts.append(ens[0][0])
            else:
                ts.append('NULL')
            tresult.append(ts)
        return render_template('translate.html', entries=tresult)
    else:
        return render_template('translate.html')

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')
        
 
if __name__ == '__main__':
    app.run(debug=True)
