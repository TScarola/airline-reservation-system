#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='air_ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define route for home page when not logged in
@app.route('/')
def  index():
    return render_template('home.html')

#Define route for user login
@app.route('/userlogin')
def userlogin():
    return render_template('userlogin.html')

#Define route for staff login
@app.route('/stafflogin')
def stafflogin():
    return render_template('stafflogin.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticate user login
@app.route('/userloginAuth', methods=['GET', 'POST'])
def userloginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s AND password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if(data):
        error = 'Yeah thats right but I havent added the next step yet'
        return render_template('userlogin.html', error=error)
    else:
        error = 'Invalid login information'
        return render_template('userlogin.html', error=error)

#Authenticate staff login
@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if(data):
        error = 'Yeah thats right but I havent added the next step yet'
        return render_template('userlogin.html', error=error)
    else:
        error = 'Invalid login information'
        return render_template('userlogin.html', error=error)

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION ***************************
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
