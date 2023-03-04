
from flask import Blueprint, appcontext_pushed,flash,send_file
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL,MySQLdb
import main 
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import send_from_directory

staff=Blueprint("staff",__name__,static_folder="static",template_folder="templates")


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','doc','docx','pdf'])



@staff.route("/staffdash/",methods=['GET','POST'])
def staff_1():

    return (render_template('staff_dash.html'))


def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
@staff.route("/upload",methods=["POST","GET"])
def upload():
    return render_template('uploadForm.html')



idstaff=0
data=''
id1=0
sub_id=0
@staff.route("/staffprofile",methods=["POST","GET"])
def profile():
    global idstaff,data,id1,sub_id
    user=main.username2
    id1=main.id
    headings=("StaffID","Staff Name","Staff Email","Course ID","Subject ID")
    

    cursor=main.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM staff WHERE staff_name = %s ', [user])
    data=cursor.fetchone()
    sub_id=data['sub_id']
    idstaff=data['staff_id']
        
    return render_template('profilestaff.html',headings=headings,data=data)


@staff.route("/uploadfile",methods=["POST","GET"])
def uploadfile():
    global idstaff
    cursor = main.mysql.connection.cursor()
    cur =main.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(main.app.config['UPLOAD_FOLDER'], filename))
                file_l="static\\uploads\\"+filename
                file_loc=f'"{file_l}"'
                cur.execute("INSERT INTO files (file_name, uploaded_on,file_location,staffid) VALUES (%s, %s,%s,%s)",[filename, now,file_l,idstaff])
                main.mysql.connection.commit()
            print(file)
        cur.close()   
        flash('File(s) successfully uploaded')   
    return redirect('/staff/upload')
 

@staff.route('/studentlist',methods=['GET','POST'])
def staff_liststudent():
    
    headings=("Student ID","Student Name","Student EMail")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT student_id,student_name,student_mail from student where sub_id1=%s or sub_id2=%s or sub_id3=%s ',(sub_id,sub_id,sub_id))
    ans=cursor1.fetchall()
    cursor1.close()
    return render_template('staff_stulist.html',headings=headings,data=ans)

@staff.route('/showfiles',methods=['GET','POST'])
def show_file():
    
    headings=("Number","File Name","Uploaded on")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM files where staffid=%s',[idstaff])
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('uploadForm.html',headings=headings,data=data)


@staff.route('/stafftest',methods=['GET','POST'])
def staff_test():

    headings=("Test ID","Test Name","Subject ID","Date and Time")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM test where sub_id=%s',[sub_id])
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('stafftest.html',headings=headings,data=data)


@staff.route('/addtest',methods=['POST'])
def insert_test():
    if request.method=='POST':
        
        testname=request.form['test_name']
        subid=request.form['subjectid']
        date=request.form['test_date']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into test(test_name,sub_id,test_date) values (%s,%s,%s)', (testname,subid,date))
        main.mysql.connection.commit()

        return render_template('stafftest.html')

@staff.route('/staffresult',methods=['GET','POST'])
def staff_results():

    headings=("Result ID","Test ID","Subject ID","Student ID","Marks")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM result where sub_id=%s',[sub_id])
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('staff_result.html',headings=headings,data=data)


@staff.route('/addresult',methods=['POST'])
def insert_result():
    if request.method=='POST':
        
        testid=request.form['testid']
        subid=request.form['subjectid']
        stuid=request.form['stuid']
        mark=request.form['marks']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into result(test_id,sub_id,stu_id,marks) values (%s,%s,%s,%s)', (testid,subid,stuid,mark))
        main.mysql.connection.commit()

        return render_template('staff_result.html')



@staff.route('/updateresult',methods=['POST'])
def update_result():
    if request.method=='POST':
        
        testid=request.form['testid']
        subid=request.form['subjectid']
        stuid=request.form['stuid']
        mark=request.form['marks']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Update result set test_id=%s,sub_id=%s,stu_id=%s,marks=%s', (testid,subid,stuid,mark))
        main.mysql.connection.commit()

        return render_template('staff_result.html')



