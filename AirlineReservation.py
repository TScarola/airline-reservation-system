#Import Flask Library
from flask import Flask, flash, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
import random

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
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    email = session['username']
    cursor = conn.cursor()
    query = 'SELECT * FROM ticket WHERE %s = customer_email AND departure_date > CURRENT_DATE'
    cursor.execute(query, (email))
    conn.commit()
    flightInfo = cursor.fetchall()
    error=None
    if request.method == 'POST':
        if request.form['cancelflight'] == 'Cancel Flight':
            dropid = request.form['dropid']
            drop = 'DELETE FROM ticket WHERE id = %s AND departure_date > (SELECT ADDDATE(CURRENT_DATE, 1) AS DateAdd)'
            cursor.execute(drop, (dropid))
            conn.commit()
            cursor.close()
            return redirect(url_for('userhome'))
            #error = 'Flight will be cancelled'
            #return render_template('userhome.html', flightInfo = flightInfo, error=error)
            #return redirect(url_for('userhome'))
    cursor.close()
    return render_template('userhome.html', flightInfo = flightInfo)

#user search and purchase tickets
@app.route('/searchpurchase', methods=['GET', 'POST'])
def searchpurchase():
    cursor = conn.cursor()
    if request.method == "POST":
        flight = request.form['q']
        search = 'SELECT * FROM flight WHERE departure_airport = %s OR arrival_airport = %s'
        cursor.execute(search, (flight, flight))
        conn.commit()
        data = cursor.fetchall()
        return render_template('searchpurchase.html', data=data)
    cursor.close()
    return render_template('searchpurchase.html')

@app.route('/purchaseAuth', methods=['GET', 'POST'])
def purchaseAuth():
    email = request.form['customer_email']
    airline = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    flight_class = request.form['class']
    card_number = request.form['card_number']
    card_exp = request.form['card_expiration']
    card_type = request.form['card_type']
    price = request.form['price']
    purchase_date = datetime.datetime.today()
    purchase_date = purchase_date.replace(microsecond=0)

    cursor = conn.cursor()
    error = None

    query = 'SELECT * FROM flight WHERE %s = airline_name AND %s = departure_date AND %s = number'
    cursor.execute(query, (airline, departure_date, flight_number))
    data = cursor.fetchone()
    if(data):
        temp_ticket_id = random.randint(0, 100000)
        check_ticket_num = 'SELECT id FROM ticket WHERE %s = airline_name AND %s = departure_date AND %s = flight_number'
        cursor.execute(check_ticket_num, (airline, departure_date, flight_number))
        conn.commit()
        ticket_exist = cursor.fetchone()
        while (ticket_exist):
            temp_ticket_id = random.randint(0, 100000)
            check_ticket_num = 'SELECT id FROM ticket WHERE %s = airline_name AND %s = departure_date AND %s = flight_number'
            cursor.execute(check_ticket_num, (airline, departure_date, flight_number))
            conn.commit()
            ticket_exist = cursor.fetchone()
        ticket_id = temp_ticket_id
        ins = 'INSERT INTO ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (ticket_id, email, departure_date, flight_number, airline, flight_class, price, card_type, card_number, card_exp, purchase_date))
        conn.commit()
        cursor.close()
        return redirect(url_for('searchpurchase'))
    else:
        flash('That flight does not exist')
        return redirect(url_for('searchpurchase'))
    
#track user spending
@app.route('/trackspending')
def trackspending():
    return render_template('trackspending.html')

#users rate and comment on previous flights
@app.route('/ratecomment', methods=['GET', 'POST'])
def ratecomment():
    email = session['username']
    cursor = conn.cursor()
    getFlight = 'SELECT airline_name, departure_date, flight_number, class, rating, comment FROM ticket NATURAL LEFT OUTER JOIN rating WHERE %s = customer_email AND departure_date < CURRENT_DATE'
    cursor.execute(getFlight, (email))
    conn.commit()
    flights = cursor.fetchall()
    if request.method == 'POST':
        #request
        comment = request.form['comment']
        rating = request.form['rating']
        airline_name = request.form['airline_name']
        departure_date = request.form['departure_date']
        flight_number = request.form['flight_number']
        #execute
        ins = 'INSERT INTO rating VALUES(%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)'
        cursor.execute(ins, (comment, rating, airline_name, departure_date, flight_number))
        #commit
        conn.commit()
        #close
        cursor.close()
        return redirect(url_for('ratecomment'))
    cursor.close()
    return render_template('ratecomment.html', flights=flights)

#route for staff home page when logged in
@app.route('/staffhome')
def staffhome():
    username = session['username']
    #cursor = conn.cursor()
    #query = 'SELECT '
    return render_template('staffhome.html')

#staff member create new flight page
@app.route('/createflight')
def createflight():
    return render_template('createflight.html')

@app.route('/createflightAuth', methods=['GET', 'POST'])
def createflightAuth():
    #get all info
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    base_price = request.form['base_price']
    plane_id = request.form['plane_id']
    status = request.form['status']

    #execute sql
    cursor = conn.cursor()
    #get airline name, flight number, departure datetime
    query = 'SELECT * FROM flight WHERE departure_date = %s AND airline_name = %s AND number = %s'
    cursor.execute(query, (departure_date, airline_name, flight_number))
    data = cursor.fetchall()
    error = None

    #check if flight is already in system
    if (data):
        error = 'This flight already exists'
        return render_template('createflight.html', error=error)
    else:
        ins = 'INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (departure_date, flight_number, airline_name, departure_airport, arrival_airport, arrival_date, base_price, plane_id, status))
        conn.commit()
        cursor.close()
        return render_template('staffhome.html')

#staff member change status of a flight
@app.route('/changestatus')
def changestatus():
    return render_template('changestatus.html')

@app.route('/changestatusAuth', methods=['GET', 'POST'])
def changestatusAuth():
    #get important flight info
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    new_status = request.form['status']
    #execute sql
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE departure_date = %s AND airline_name = %s AND number = %s'
    cursor.execute(query, (departure_date, airline_name, flight_number))
    data = cursor.fetchall()
    error = None
    #check if flight is in system
    if (data):
        upd = 'UPDATE flight SET status = %s WHERE departure_date = %s AND airline_name = %s AND number = %s'
        cursor.execute(upd, (new_status, departure_date, airline_name, flight_number))
        conn.commit()
        cursor.close()
        return render_template('staffhome.html')
    else:
        error = 'This flight is not in the system'
        return render_template('changestatus.html', error=error)

#staff member add new airport page
@app.route('/addairport')
def addairport():
    return render_template('addairport.html')

@app.route('/addairportAuth', methods=['GET', 'POST'])
def addairportAuth():
    #get all info
    code = request.form['code']
    name = request.form['name']
    city = request.form['city']
    country = request.form['country']
    ap_type = request.form['type']
    #execute sql
    cursor = conn.cursor()
    query = 'SELECT code FROM airport WHERE code = %s'
    cursor.execute(query, (code))
    data = cursor.fetchone()
    error = None
    #check if airport is already in system
    if (data):
        error = 'This airport already exists'
        return render_template('addairport.html')
    else:
        ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (code, name, city, country, ap_type))
        conn.commit()
        cursor.close()
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
