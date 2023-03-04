from flask import Blueprint,render_template
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import main 

admin=Blueprint("admin",__name__,static_folder="static",template_folder="templates")

@admin.route('/admin',methods=['GET','POST'])
def admin_1():

    return render_template('admin_dash.html')


@admin.route('/staff',methods=['GET','POST'])
def admin_staff():

    headings=("Staff ID","Staff Name","Staff EMail","Course ID","Subject ID")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM staff')
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_staff.html',headings=headings,data=data)

@admin.route('/student',methods=['GET','POST'])
def admin_student():
    
    headings=("Student ID","Student Name","Student EMail","Course ID","Subject 1","Subject2","Sunject3")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM student')
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_student.html',headings=headings,data=data)

@admin.route('/course',methods=['GET','POST'])
def admin_course():
    
    headings=("Course ID","Course Name")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM course')
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_course.html',headings=headings,data=data)

@admin.route('/subject',methods=['GET','POST'])
def admin_subject():
    
    headings=("Subject ID","Subject Name","Course ID")
    cursor1=main.mysql.connection.cursor()
    cursor1.execute('SELECT *FROM subject')
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_subject.html',headings=headings,data=data)

@admin.route('/addstaff',methods=['POST'])
def insert_staff():
    if request.method=='POST':
        name=request.form['name']
        mail=request.form['email']
        course=request.form['courseid']
        subject=request.form['subjectid']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into staff(staff_name,staff_mail,course_id,sub_id) values (%s,%s,%s,%s)', (name,mail,course,subject))
        main.mysql.connection.commit()

        return render_template('admin_staff.html')

@admin.route('/editstaff',methods=['POST'])
def update_staff():
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        mail=request.form['email']

        course=request.form['courseid']
        subject=request.form['subjectid']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute(' Update staff set staff_name=%s,staff_mail=%s, course_id=%s,sub_id=%s where staff_id=%s', (name,mail,course,subject,id))
        main.mysql.connection.commit()

        return render_template('admin_staff.html')

@admin.route('/deletestaff',methods=['POST'])
def delete_staff():
    if request.method=='POST':
        id=request.form['id']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute(' Delete from staff  where staff_id=%s', [id])
        main.mysql.connection.commit()

        return render_template('admin_staff.html')

    

@admin.route('/addstudent',methods=['POST'])
def insert_student():
    if request.method=='POST':
        name=request.form['name']
        mail=request.form['email']
        course=request.form['courseid']
        subject1=request.form['subjectid1']
        subject2=request.form['subjectid2']
        subject3=request.form['subjectid3']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into student(student_name,student_mail,course_id,sub_id1,sub_id2,sub_id3) values (%s,%s,%s,%s,%s,%s)', (name,mail,course,subject1,subject2,subject3))
        main.mysql.connection.commit()

        return render_template('admin_student.html')

@admin.route('/editstudent',methods=['POST'])
def update_student():
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        mail=request.form['email']
        course=request.form['courseid']
        subject1=request.form['subjectid1']
        subject2=request.form['subjectid2']
        subject3=request.form['subjectid3']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Update student set student_name=%s,student_mail=%s, course_id=%s,sub_id1=%s,sub_id2=%s,sub_id1=3=%s where student_id=%s', (name,mail,course,subject1,subject2,subject3,id))
        main.mysql.connection.commit()

        return render_template('admin_student.html')

@admin.route('/deletestudent',methods=['POST'])
def delete_student():
    if request.method=='POST':
        id=request.form['id']

        cursor1=main.mysql.connection.cursor()
        cursor1.execute(' Delete from student  where student_id=%s', (id))
        main.mysql.connection.commit()

        return render_template('admin_student.html')



@admin.route('/addsubject',methods=['POST'])
def insert_subject():
    if request.method=='POST':
        
        subject=request.form['subject']
        course=request.form['courseid']
        

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into subject(sub_name,course_id) values (%s,%s)', (subject,course))
        main.mysql.connection.commit()

        return render_template('admin_subject.html')


@admin.route('/addcourse',methods=['POST'])
def insert_course():
    if request.method=='POST':
        
        
        course=request.form['course']
        

        cursor1=main.mysql.connection.cursor()
        cursor1.execute('Insert into course(course_name) values (%s)', [course])
        main.mysql.connection.commit()

        return render_template('admin_course.html')