from flask import Flask,render_template,request,session,url_for,flash,redirect
from mysql.connector import connect
import os
from Query import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yoiusaiudiuaiosdoiasd'


@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('index.html')
    else: return redirect(url_for('login'))

@app.route('/logout')
def logout():
    app.secret_key = os.urandom(32)
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if 'user' not in session:
        return render_template('login.html')
    else: return redirect(url_for('home'))

@app.route('/validation', methods=['POST'])
def validation():
    
    session.pop('_flashes', None)
    username  = request.form['username']
    password  = request.form['password']

    if username == 'user' and password == 'admin':
        
        query = Query('student')
        data = query.getData()

        session['loggedin'] = True
        session['user'] = username
        session['students_data'] = data
        return redirect(url_for('home'))
    else:
        flash("Invalid username and password")
    return redirect(url_for('login'))


@app.route("/insert-data", methods=['POST'])
def insertData():
    session.pop('_flashes', None)
    query = Query('student', 
        idno = request.form['idno'],
        lastname = request.form['lastname'],
        firstname = request.form['firstname'],
        course = request.form['course'],
        level = request.form['level'],
    )       
    data = query.addQuery()

    if data:
        flash("Added Successfully")
        session['students_data'] = query.getData()
    else:
        flash("Data not inserted something occured")
    return redirect(url_for('home'))

@app.route("/deleting", methods=['POST'])
def deleteData():
    session.pop('_flashes', None)

    idno = request.form['id']
    
    if id:
        query = Query('student', idno=idno)
        data = query.deleteQuery()

        if data:
            flash("Deleted Successfully")
            session['students_data'] = query.getData()
    else:
        flash("Something was wrong please try again.")
    return redirect(url_for('home'))


@app.route("/editing", methods=['POST'])
def editData():
    session.pop('_flashes', None)

    idno = request.form['id']

    if idno:
        query = Query('student', idno=idno)
        data = query.getSingleData()

        if data:
            session['data'] = data
            return render_template('edit.html')
    else:
        flash('Something was wrong please try again.')
    return redirect(url_for('home'))


@app.route('/updated', methods=['POST'])
def updateData():
    session.pop('_flashes', None)

    
    query = Query('student', 
        idno = request.form['idno'],
        lastname = request.form['lastname'],
        firstname = request.form['firstname'],
        course = request.form['course'],
        level = request.form['level'],
    )

    row = query.updateQuery()

    if row:
        flash('Updated succesfully')
        session['students_data'] = query.getData()
    else: flash('Not updated ')
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)