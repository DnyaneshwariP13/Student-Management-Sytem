from flask import Blueprint,render_template,send_file
import MySQLdb.cursors
from flask_mysqldb import MySQL
import main
from staff import*

student=Blueprint("student",__name__,static_folder="static",template_folder="templates")

@student.route('/studentdash/',methods=['GET','POST'])
def studentd():

    return render_template('student_dash.html')

idstudent=0
subid1=0
subid2=0
subid3=0
data2=''
id1=0
@student.route("/studentprofile",methods=["POST","GET"])
def profilestu():
    global data2,id1,idstudent,subid1,subid2,subid3
    user2=main.username2
    id1=main.id
    headings=("Student ID","Student Name","Student email","Course ID","Subject ID1","Subject ID2","Subject ID3")

    cursor=main.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT *FROM student WHERE student_name = %s ', [user2])
    data2=cursor.fetchone()
    idstudent=data2['student_id']
    subid1=data2['sub_id1']
    subid2=data2['sub_id2']
    subid3=data2['sub_id3']
    return render_template('profilestudent.html',headings=headings,data=data2)

@student.route('/files',methods=['GET','POST'])
def files_student():
    
    headings=("Number","File Name","Uploaded on")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM files')
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('student_file.html',headings=headings,data=data)

data1=''
id=0
@student.route('/returnFile/',methods=["POST","GET"])
def download_file():
    global data1,id
    if request.method=='POST' and 'id' in request.form :
        id=request.form['id']
    
    cursor=main.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT  *from  files WHERE file_id=%s ',[id])
    data1=cursor.fetchone()
    filel=data1['file_location']
    return send_file(filel, as_attachment=True)
    #return render_template('student_file.html',data=filel)

@student.route('/staffDir',methods=['GET','POST'])
def st_student():
    global subid1,subid2,subid3
    headings=("StaffID","Staff Name","Staff Email","Course ID","Subject ID")
    cursor2=main.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT * FROM staff WHERE sub_id = %s or sub_id = %s or sub_id = %s  ', [subid1,subid2,subid3])
    data=cursor2.fetchall()
    cursor2.close()
    return render_template('student_staff.html',headings=headings,data=data)

@student.route('/stutests',methods=['GET','POST'])
def student_test():
    global subid1,subid2,subid3
    headings=("Test ID","Test Name","Subject ID","Date and Time")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM test where sub_id = %s or sub_id = %s or sub_id = %s',[subid1,subid2,subid3])
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('studenttest.html',headings=headings,data=data)

@student.route('/studentsresult',methods=['GET','POST'])
def student_results():
    global subid1,subid2,subid3
    headings=("Result ID","Test ID","Subject ID","Student ID","Marks")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM result where sub_id=%s or sub_id = %s or sub_id = %s',[subid1,subid2,subid3])
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('student_result.html',headings=headings,data=data)