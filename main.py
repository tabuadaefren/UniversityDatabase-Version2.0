from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

# CREATE STUDENT OBJECT/STRUCTURE
class Student(object):
    def __init__(self, idnum, firstname, lastname, middlename,sex, Course, Yr):
        self.id_no = idnum
        self.f_name = firstname
        self.l_name = lastname
        self.mid = middlename
        self.sex = sex
        self.course = Course
        self.Yr = Yr

# INITIAL DATABASE CREATION
conn = sql.connect('database.db')
conn.execute(
    '''CREATE TABLE IF NOT EXISTS student(IDNum TEXT PRIMARY KEY  NOT NULL CHECK(length(IDNum)=9), 
    FName TEXT  CHECK(length(FName)>0 AND length(FName)<=20 ), 
    LName TEXT CHECK(length(LName)>0 AND length(LName)<=20 ), 
    MName TEXT CHECK(length(MName)>0 AND length(MName)<=20 ) , 
    Sex TEXT CHECK(length(Sex)=1), 
    Course TEXT CHECK(length(Course)>0 AND length(Course)<=20 ), 
    YrLevel INTEGER CHECK(length(YrLevel)=1))''')

conn.close()

# -- HOME PAGE --
@app.route("/",methods = ['POST','GET'])
def main():
    return render_template("main.html")

# -- Methods for Students --

#--------------------------------------------------
# -- Manage Students - main method --
@app.route("/students",methods = ['POST','GET'])
def indexStudents():
    return render_template("index.html")



# -- ADD METHODS --
@app.route("/add",methods = ['POST','GET'])
def add():
    return render_template("add.html")

@app.route("/add_submit",methods = ['POST','GET'])
def add_submit():
    if request.method == "POST":
        
        try:
            
            id_number = request.form['ID_Num']
            firstname = request.form['F_Name']
            lastname = request.form['L_Name']
            middle = request.form['M_Name']
            sex =request.form['sex']
            course = request.form['course']
            Yr = request.form['Yr_Level']
            
            stud = Student(id_number,firstname,lastname,middle,sex,course,Yr)
            print "array"
            with sql.connect("database.db") as conn:
                print "connect"
                cur = conn.cursor()
                cur.execute("INSERT INTO student(IDNum, FName, LName, MName, Sex, Course,YrLevel) VALUES(?,?,?,?,?,?,?)",
                    (stud.id_no, stud.f_name, stud.l_name, stud.mid, stud.sex, stud.course,stud.Yr))
                conn.commit()
                msg= "Adding Successful!"
        except:
        	print " ERROR!"
        	conn.rollback()
        	msg = "Adding failed! "

        finally:
        	print "Final Stage"
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
            print "entered ID"
            id_number = request.form['ID_Num']
            print id_number
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    print row
                    if row[0] == id_number:
                        print "partial in del"
                        cur.execute("DELETE FROM student WHERE IDNum = ?", (id_number,))
                        print "before commit"
                        conn.commit()
                        print "committed"
                        msg = "Successfully Deleted"
                        flag=1
                        break
                    else:
                        print "error delete"
                        flag=0
                        msg = "Error! Student not found."
                        
                        
        except:
            msg = "Fail to delete"
            print "Failed to delete!"
        finally:
            if flag == 1:
                print "flag 1"
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                rows = cur.fetchall()
                print rows
            else:
                print "flag 0"
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
            print "meeeee"
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        print row
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
            print "enter try"
            
            id_old = request.form['ID_old']
            id_new = request.form['ID_Num']
            print id_old
            firstname = request.form['F_Name']
            lastname = request.form['L_Name']
            middle = request.form['M_Name']
            sex = request.form['sex']
            course = request.form['course']
            Yr = request.form['Yr_Level']

            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    print row

                    if row[0] == id_old:
                        cur.execute("UPDATE student set FName = ?, LName = ?, MName = ?,  Sex = ?, Course = ?, YrLevel = ? where IDNum = ?",
                            ( firstname, lastname, middle, sex, course,Yr,id_old))
                        conn.commit()
                        cur.execute("UPDATE student set IDNum=? where FName = ? and LName = ?",
                            (id_new, firstname, lastname))
                        conn.commit()
                        msg = "successfully UPDATED"
                        break
                    
        except:
            print "Fail to update"
            msg = "FAIL to UPDATE"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            return render_template("update_success.html", rows=rows, msg=msg)
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
            count=0
            SeachKey = request.form['SearchKey']
            
            with sql.connect("database.db") as conn:
                
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        print row
                        copied = row
                        print "search successful"
                        msg = "Search successful!"
                        break
                    else:
                        print "Error search"
                        msg = "Error! Student not found."
                        copied = " "

        except:
            msg = "ERROR"
            copied=" "
        finally:
            return render_template("search_result.html", msg=msg, copied=copied, )
            conn.close()
#---------------------------------------------------
#End Manage Students



# Methods for Courses
#----------------------------------------------------
# Manage Courses
@app.route("/courses",methods = ['POST','GET'])
def indexCourses():
    return render_template("index-courses.html")


# -- ADD METHODS --
@app.route("/add_course",methods = ['POST','GET'])
def add_course():
    return render_template("add.html")

@app.route("/add_submit_course",methods = ['POST','GET'])
def add_submit_course():
    if request.method == "POST":
        
        try:
            
            id_number = request.form['ID_Num']
            firstname = request.form['F_Name']
            lastname = request.form['L_Name']
            middle = request.form['M_Name']
            sex =request.form['sex']
            course = request.form['course']
            Yr = request.form['Yr_Level']
            
            stud = Student(id_number,firstname,lastname,middle,sex,course,Yr)
            print "array"
            with sql.connect("database.db") as conn:
                print "connect"
                cur = conn.cursor()
                cur.execute("INSERT INTO student(IDNum, FName, LName, MName, Sex, Course,YrLevel) VALUES(?,?,?,?,?,?,?)",
                    (stud.id_no, stud.f_name, stud.l_name, stud.mid, stud.sex, stud.course,stud.Yr))
                conn.commit()
                msg= "Adding Successful!"
        except:
            print " ERROR!"
            conn.rollback()
            msg = "Adding failed! "

        finally:
            print "Final Stage"
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            return render_template("add_result.html", rows=rows, msg=msg,)
            conn.close()
# -- End Add Methods --


# -- DISPLAY TABLE -view table --
@app.route("/view_course",methods = ['POST','GET'])
def view_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    return render_template("add_result.html", rows=rows)
    conn.close()


# -- DELETE METHODS --
@app.route("/delete_course", methods = ['POST', 'GET'])
def delete_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows_del = cur.fetchall()
    conn.close()
    return render_template("delete.html", rows=rows_del)

@app.route("/delete_result_course",methods = ['POST','GET'])
def delete_result_course():
    if request.method == "POST":
        try:
            print "entered ID"
            id_number = request.form['ID_Num']
            print id_number
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    print row
                    if row[0] == id_number:
                        print "partial in del"
                        cur.execute("DELETE FROM student WHERE IDNum = ?", (id_number,))
                        print "before commit"
                        conn.commit()
                        print "committed"
                        msg = "Successfully Deleted"
                        flag=1
                        break
                    else:
                        print "error delete"
                        flag=0
                        msg = "Error! Student not found."
                        
                        
        except:
            msg = "Fail to delete"
            print "Failed to delete!"
        finally:
            if flag == 1:
                print "flag 1"
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                rows = cur.fetchall()
                print rows
            else:
                print "flag 0"
                rows = " "
            return render_template("add_result.html", rows=rows, msg=msg,)
        conn.close()
# -- End of Delete Methods --


# -- UPDATE METHODS --
@app.route("/update_course", methods=['POST', 'GET'])
def update_course():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    return render_template("update.html", rows=rows)

@app.route("/update_search_course",methods = ['POST', 'GET'])
def update_search_course():
    if request.method == "POST":
        try:
            id_number = request.form['ID_Num']
            print "meeeee"
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        print row
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

@app.route("/update_submit_course",methods = ['POST', 'GET'])
def update_submit_course():
    if request.method =="POST":
        
        try:
            print "enter try"
            
            id_old = request.form['ID_old']
            id_new = request.form['ID_Num']
            print id_old
            firstname = request.form['F_Name']
            lastname = request.form['L_Name']
            middle = request.form['M_Name']
            sex = request.form['sex']
            course = request.form['course']
            Yr = request.form['Yr_Level']

            with sql.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    print row

                    if row[0] == id_old:
                        cur.execute("UPDATE student set FName = ?, LName = ?, MName = ?,  Sex = ?, Course = ?, YrLevel = ? where IDNum = ?",
                            ( firstname, lastname, middle, sex, course,Yr,id_old))
                        conn.commit()
                        cur.execute("UPDATE student set IDNum=? where FName = ? and LName = ?",
                            (id_new, firstname, lastname))
                        conn.commit()
                        msg = "successfully UPDATED"
                        break
                    
        except:
            print "Fail to update"
            msg = "FAIL to UPDATE"
        finally:
            conn = sql.connect("database.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            return render_template("update_success.html", rows=rows, msg=msg)
            conn.close()
# -- End of Update Methods --


# -- SEARCH METHODS --
@app.route("/search_course",methods = ['POST', 'GET'])
def search_course():
    return render_template("search.html")

@app.route("/search_input_course",methods = ['POST', 'GET'])
def search_input_course():
    if request.method == "POST":
        try:
            count=0
            id_number = request.form['ID_Num']
            print "meeeee"
            with sql.connect("database.db") as conn:
                print "connected"
                cur = conn.cursor()
                cur.execute("SELECT * FROM student")
                for row in cur.fetchall():
                    if row[0] == id_number:
                        print row
                        copied = row
                        print "search successful"
                        msg = "Search successful!"
                        break
                    else:
                        print "Error search"
                        msg = "Error! Student not found."
                        copied = " "

        except:
            msg = "ERROR"
            copied=" "
        finally:
            return render_template("search_result.html", msg=msg, copied=copied, )
            conn.close()


#----------------------------------------------------
# End Manage Courses
if __name__ == "__main__":
    app.run(debug=True)