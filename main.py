from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


# INITIAL DATABASE CREATION

#Create  student Table
conn = sql.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS student(
    IDNum TEXT PRIMARY KEY  NOT NULL, 
    FName TEXT, 
    MName TEXT,
    LName TEXT, 
    Sex TEXT, 
    Course TEXT REFERENCES courses(CourseID) ON DELETE RESTRICT, 
    YrLevel INTEGER)''')

conn.execute('''CREATE TABLE IF NOT EXISTS courses(
    CourseID TEXT PRIMARY KEY  NOT NULL, 
    CourseTitle TEXT,
    College TEXT )''')

conn.close()

#Create course Table

# -- HOME PAGE --
@app.route("/",methods = ['POST','GET'])
def main():
    return render_template("main.html")

# -- Methods for Students --

#--------------------------------------------------
# -- Manage Students - main method --
@app.route("/students",methods = ['POST','GET'])
def indexStudents():
    return render_template("index-students.html")



# -- ADD METHODS --
@app.route("/add",methods = ['POST','GET'])
def add():
    return render_template("add.html")

@app.route("/add_submit",methods = ['POST','GET'])
def add_submit():
    if request.method == "POST":
        try:
            id_number = request.form['ID_Num']
            firstname = request.form['F_Name'].upper()
            middle = request.form['M_Name'].upper()
            lastname = request.form['L_Name'].upper()
            sex =request.form['sex'].upper()
            course = request.form['course'].upper()
            Yr = request.form['Yr_Level'].upper()
            
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys=ON")
                cur.execute("INSERT INTO student(IDNum, FName, MName,  LName, Sex, Course,YrLevel) VALUES(?,?,?,?,?,?,?)",
                    (id_number,firstname,middle,lastname,sex,course,Yr))
                conn.commit()
                msg= "Adding Successful!"
        except:
        	conn.rollback()
        	msg = "Error adding due to foreign key constraint."

        finally:
        	conn = sql.connect("database.db")
        	conn.row_factory = sql.Row
        	cur = conn.cursor()
        	cur.execute("SELECT * FROM student")
        	rows = cur.fetchall()
        	return render_template("add_result.html", rows=rows, msg=msg,)
        	conn.close()
# -- End Add Methods --


# -- DISPLAY TABLE -view table --
@app.route("/view",methods = ['POST','GET'])
def view():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    return render_template("add_result.html", rows=rows)
    conn.close()


# -- DELETE METHODS --
@app.route("/delete", methods = ['POST', 'GET'])
def delete():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows_del = cur.fetchall()
    conn.close()
    return render_template("delete.html", rows=rows_del)

@app.route("/delete_result",methods = ['POST','GET'])
def delete_result():
    if request.method == "POST":
        try:
            id_number = request.form['ID_Num']
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        cur.execute("DELETE FROM student WHERE IDNum = ?", (id_number,))
                        conn.commit()
                        msg = "Successfully Deleted"
                        flag=1
                        break
                    else:
                        flag=0
                        msg = "Error! Student not found."
        except:
            msg = "Fail to delete"
            
        finally:
            if flag == 1:
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                rows = cur.fetchall()
            else:
                rows = " "
            return render_template("add_result.html", rows=rows, msg=msg,)
        conn.close()
# -- End of Delete Methods --


# -- UPDATE METHODS --
@app.route("/update", methods=['POST', 'GET'])
def update():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    return render_template("update.html", rows=rows)

@app.route("/update_search",methods = ['POST', 'GET'])
def update_search():
    if request.method == "POST":
        try:
            id_number = request.form['ID_Num']
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        copied = row
                        msg = " Student Found!"
                        flag = 1
                        break
                    else:
                        msg = "Error! Student not found."
                        flag=0
                        copied = " "

        except:
            msg1 = "ERROR"
            msg2 = " "
            copied = " "
        finally:
            if flag == 1:
                return render_template("update_info.html", msg =msg, copied=copied, id_number=id_number, )
                conn.close()
            else:
                return render_template("update_search_fail.html", msg =msg, copied=copied, id_number=id_number, )
                conn.close()

@app.route("/update_submit",methods = ['POST', 'GET'])
def update_submit():
    if request.method =="POST":
        try:
            id_old = request.form['ID_old']
            firstname = request.form['F_Name'].upper()
            lastname = request.form['L_Name'].upper()
            middle = request.form['M_Name'].upper()
            sex = request.form['sex'].upper()
            course = request.form['course'].upper()
            Yr = request.form['Yr_Level'].upper()
            
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_old:
                        if(len(course)>0):
                            print("before pragma")
                            cur.execute("PRAGMA foreign_keys=ON")
                            print("entered after pragma")
                            cur.execute("UPDATE student set Course = ? where IDNum = ?",( course, id_old))
                        if(len(firstname)>0):
                            cur.execute("UPDATE student set FName = ? where IDNum = ?",( firstname, id_old))
                        if(len(lastname)>0):
                            cur.execute("UPDATE student set LName = ? where IDNum = ?",( lastname, id_old))
                        if(len(middle)>0):
                            cur.execute("UPDATE student set MName = ? where IDNum = ?",( middle, id_old))
                        if(len(sex)>0):
                            cur.execute("UPDATE student set Sex = ? where IDNum = ?",( sex, id_old))
                        if(len(Yr)>0):
                            cur.execute("UPDATE student set YrLevel = ? where IDNum = ?",( Yr, id_old))
                        conn.commit()
                        msg = "successfully UPDATED"
                        break
        except:
            msg = "FAIL to UPDATE"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            return render_template("update_success.html", rows=rows, )
            conn.close()
# -- End of Update Methods --


# -- SEARCH METHODS --
@app.route("/search",methods = ['POST', 'GET'])
def search():
    return render_template("search.html")

@app.route("/search_input",methods = ['POST', 'GET'])
def search_input():
    if request.method == "POST":
        try:
            print("try entered")
            count=0
            SearchKey = request.form['SearchKey'].upper()
            print(SearchKey)
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                print("sql execute")
                cur.execute("SELECT * FROM student where IDNum = ? or FName = ? or LName=? or MName=?  or Sex=? or YrLevel=? or Course=?", (SearchKey, SearchKey, SearchKey, SearchKey, SearchKey, SearchKey, SearchKey ))
                print("finish search database")
                row = cur.fetchall()
                print("entered in success")
                print(row)
                print(len(row))
        except:
            print("entered in failed")
        finally:
            if(len(row)<1):
                msg="Student not found!"
                print("entered if")
                row= " "
            else:
                msg="Search successful!"
                print("entered else")
            return render_template("search_result.html", msg=msg, row=row,)
            conn.close()
        
#---------------------------------------------------
#End Manage Students



# Methods for Manage Courses
#----------------------------------------------------

# Manage Courses
@app.route("/courses",methods = ['POST','GET'])
def indexCourses():
    return render_template("index-courses.html")


# -- ADD METHODS --
@app.route("/add_course",methods = ['POST','GET'])
def add_course():
    return render_template("add-course.html")

@app.route("/add_submit_course",methods = ['POST','GET'])
def add_submit_course():
    if request.method == "POST":
        
        try:
            
            crs_ID = request.form['course-ID'].upper()
            crs_title = request.form['course-title'].upper()
            crs_college = request.form['course-college'].upper()
            
            print("array")
            with sql.connect("database.db") as conn:
                print("connect")
                cur = conn.cursor()
                cur.execute("INSERT INTO courses(CourseID, CourseTitle, College) VALUES(?,?,?)",
                    (crs_ID,crs_title,crs_college))
                conn.commit()
                print("success stage1")
                msg= "Adding Course Successful!"
        except:
            print(" ERROR!")
            conn.rollback()
            msg = "Adding Course Failed! "

        finally:
            print("Final Stage")
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            return render_template("add_result-course.html", rows=rows, msg=msg,)
            conn.close()
# -- End Add Methods --


# -- DISPLAY TABLE -view table --
@app.route("/view_course",methods = ['POST','GET'])
def view_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    return render_template("add_result-course.html", rows=rows)
    conn.close()

# -- DELETE METHODS --
@app.route("/delete_course", methods = ['POST', 'GET'])
def delete_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows_del = cur.fetchall()
    conn.close()
    return render_template("delete-course.html", rows=rows_del)

@app.route("/delete_result_course",methods = ['POST','GET'])
def delete_result_course():
    if request.method == "POST":
        try:
            print("entered ID")
            crs_id = request.form['crs_ID'].upper()
            print(crs_id)
            with sql.connect("database.db") as conn:
                print("connected")
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    print(row)
                    if row[0] == crs_id:
                        print("course found")
                        flag=2
                        cur.execute("PRAGMA foreign_keys=ON")
                        cur.execute("DELETE FROM courses WHERE CourseID = ?", (crs_id,))
                        print("before commit")
                        conn.commit()
                        print("committed")
                        msg = "Successfully Deleted"
                        flag=1
                        break
                    else:
                        print("not found")
                        flag=0
                        msg = "Error! Course not found."
                        
                        
        except:
            msg = "Error! Foreign key constraint."
            print("Failed to delete!")
        finally:
            if flag>0:
                print("flag = " ,flag)
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                rows = cur.fetchall()
                print(rows)
            else:
                print(" flag = " ,flag)
                rows = " "
            return render_template("add_result-course.html", rows=rows, msg=msg,)
        conn.close()
# -- End of Delete Methods --


# -- UPDATE METHODS --
@app.route("/update_course", methods=['POST', 'GET'])
def update_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    return render_template("update-course.html", rows=rows)

@app.route("/update_search_course",methods = ['POST', 'GET'])
def update_search_course():
    if request.method == "POST":
        try:
            crs_ID = request.form['courseID'].upper()
            print("meeeee")
            with sql.connect("database.db") as conn:
                print("connected")
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    if row[0] == crs_ID:
                        print("found")
                        print(row)
                        copied = row
                        msg = " Student Found!"
                        flag = 1
                        break
                    else:
                        msg = "Error! Student not found."
                        flag=0
                        copied = " "
        except:
            msg1 = "ERROR"
            msg2 = " "
            copied = " "
        finally:
            if flag == 1:
                return render_template("update_info-course.html", msg =msg, copied=copied,  )
                conn.close()
            else:
                conn = sql.connect("database.db")
                conn.row_factory= sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                rows = cur.fetchall()
                return render_template("update_search_fail-course.html", msg =msg, rows=rows,  )
                conn.close()

@app.route("/update_submit_course",methods = ['POST', 'GET'])
def update_submit_course():
    if request.method =="POST":
        
        try:
            print("enter try")
            crs_ID_old = request.form['crsID_old'].upper()
            crs_ID = request.form['crsID'].upper()
            crs_title = request.form['crsTitle'].upper()
            college = request.form['college'].upper()
            print(crs_ID_old)
            

            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses")
                for row in cur.fetchall():
                    print(row)

                    if row[0] == crs_ID_old:
                        if(len(crs_title)>0):
                            print("before update title")
                            cur.execute("UPDATE courses set CourseTitle = ? where CourseID = ?",( crs_title, crs_ID_old))
                            print("after update title")
                        if(len(college)>0):
                            print("before update college")
                            cur.execute("UPDATE courses set College = ? where CourseID = ?",( college, crs_ID_old))
                            print("after update college")
                        if(len(crs_ID)>0):
                            print("before pragma")
                            cur.execute("PRAGMA foreign_keys=ON")
                            print("after pragma")
                            cur.execute("UPDATE courses set CourseID = ? where CourseID = ?",( crs_ID, crs_ID_old))
                            print("after update")   
                        conn.commit()
                        msg = "Successfully Udated"
                        break
        except:
            print("Fail to update")
            msg = "FAILED TO UPDATE"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            return render_template("update_success-course.html", rows=rows, msg=msg)
            conn.close()
# -- End of Update Methods --


# -- SEARCH METHODS --
@app.route("/search_course",methods = ['POST', 'GET'])
def search_course():
    return render_template("search-course.html")

@app.route("/search_input_course",methods = ['POST', 'GET'])
def search_input_course():
    if request.method == "POST":
        try:
            print("try entered")
            count=0
            SearchKey = request.form['SearchKey'].upper()
            print(SearchKey)
            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                print("sql execute")
                cur.execute("SELECT * FROM courses where CourseID = ? or CourseTitle = ? or College=?", (SearchKey, SearchKey, SearchKey ))
                print("finish search database")
                row = cur.fetchall()
                print("entered in success")
                print(row)
                print(len(row))
        except:
            print("entered in failed")
        finally:
            if(len(row)<1):
                msg="Student not found!"
                print("entered if")
                row= " "
            else:
                msg="Search successful!"
                print("entered else")
            return render_template("search_result-course.html", msg=msg, row=row,)
            conn.close()
#----------------------------------------------------
# End Manage Courses


if __name__ == "__main__":
    app.run(debug=True)
    