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
def home():
    return render_template('home.html')

#Define route for user login
@app.route('/userlogin')
def userlogin():
    return render_template('userlogin.html')

#Define route for staff login
@app.route('/stafflogin')
def stafflogin():
    return render_template('stafflogin.html')

#Define route for registering new user
@app.route('/userregister')
def userregister():
    return render_template('userregister.html')

#Define route for registering new staff member
@app.route('/staffregister')
def staffregister():
    return render_template('staffregister.html')

#Authenticate user login
@app.route('/userloginAuth', methods=['GET', 'POST'])
def userloginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    #execute SQL query
    query = 'SELECT * FROM customer WHERE email = %s AND password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    #check if login info is in database
    if(data): 
        #start new user session if it is
        session['username'] = username
        return redirect(url_for('userhome'))
    else: #raise error otherwise
        error = 'Invalid login information'
        return render_template('userlogin.html', error=error)

#Authenticate staff login
@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
    username = request.form['username']
    password = request.form['password']
    #execute sql query
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None
    #check if login info is in database
    if(data):
        #start new staff session if it is
        session['username'] = username
        return redirect(url_for('staffhome'))
    else:
        #raise error otherwise
        error = 'Invalid login information'
        return render_template('stafflogin.html', error=error)

#Authenticate new user register
@app.route('/userregisterAuth', methods=['GET', 'POST'])
def userregisterAuth():
    #get all user information
    email = request.form['username']
    password = request.form['password']
    name = request.form['name']
    phone_number = request.form['phone_number']
    date_of_birth = request.form['date_of_birth']
    city = request.form['city']
    state = request.form['state']
    building_number = request.form['building_number']
    street = request.form['street']
    passport_country = request.form['passport_country']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']

    #get user email from sql query
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query,(email))
    data = cursor.fetchone()
    error = None

    #check if email is already in use
    if(data):
        error = 'This user already exists'
        return render_template('userregister.html', error = error)
    else:
        #add to database
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, password, name, building_number, street, city, state, phone_number, date_of_birth, passport_country, passport_expiration, passport_number))
        conn.commit()
        cursor.close()
        return render_template('home.html')

#Authenticate new staff register
@app.route('/staffregisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
    #get all information
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    phone_number = request.form['phone_number']
    airline_name = request.form['airline_name']

    #get staff username 
    cursor = conn.cursor()
    query = 'SELECT * FROM staff WHERE username = %s'
    cursor.execute(query,(username))
    data = cursor.fetchone()
    error = None

    #check if the username is in use
    if(data):
        error = 'This staff already exists'
        return render_template('staffregister.html', error = error)
    else:
        #add to database
        ins = 'INSERT INTO staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, airline_name, password, first_name, last_name, date_of_birth, phone_number))
        conn.commit()
        cursor.close()
        return render_template('home.html')

#route for user home page when logged in
@app.route('/userhome')
def userhome():
    email = session['username']
    cursor = conn.cursor()
    query = 'SELECT departure_date, flight_number, airline_name FROM ticket WHERE %s = customer_email'
    cursor.execute(query, (email))
    flightInfo = cursor.fetchall()
    cursor.close()
    return render_template('userhome.html', flightInfo = flightInfo)

#view user flights
#@app.route('/userFlights')
#def userFlights():
    #username = session['username']
    #return render_template('userflights.html')

#route for staff home page when logged in
@app.route('/staffhome')
def staffhome():
    username = session['username']
    return render_template('staffhome.html')

#logout
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION ***************************
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
