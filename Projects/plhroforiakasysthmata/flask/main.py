from flask import Flask, render_template, redirect, session,request
from pymongo import MongoClient
import random




app=Flask(__name__)

mongo=MongoClient("mongodb://mongodb:27017")
db=mongo["DigitalAirlines"]
users=db["users"]
reservations=db["reservations"]
flights=db["flights"]
@app.route('/')
def index():
    return None

data1 = {
    "username": "Menelaos",
    "surname": "Menelaou",
    "email": "menelaos@example.com",
    "password": "1234",
    "placeofbirth":"Greece",
    "passportcode":"696969",
    "role":"admin"
}
users.insert_one(data1)

#Register
@app.route('/signup', methods=['POST'])
def registration():
   username = request.form.get('username')
   surname = request.form.get('surname')
   email = request.form.get('email')
   password = request.form.get('password')
   placeofbirth=request.form.get('placeofbirth')
   passportcode=request.form.get('passportcode')

   if not username or not surname or not email or not password or not placeofbirth or not passportcode:
      return "Please fill in all the required fields."
   existing_user = users.find_one({'$or': [{'username': username}, {'email': email}]})
   if existing_user:
        return "Name or email already exists. Please choose a different one."
   
   newuser = {
        'username': username,
        'password': password,
        'email': email,
        'role': 'user'
    }
   users.insert_one(newuser)
   return "Register Succesful"

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve user input from the login form
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = users.find_one({'email': email, 'password': password})
        # Perform authentication, e.g., check if the username and password match
        if  existing_user is not None:
            # Store user session data
            return ("Login succesful")
        else:
            return ('Invalid email or password. Please try again.')

#Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()

    return redirect('/login')

#Flight Search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        fro = request.form.get('from')
        to = request.form.get('to')
        date=request.form.get('date')
        
         
        results=flights.find({'from': fro})
        data = []
        for i in results:
         result = { 'from': result['from'], 'to': result['to'],'date':result['date'], 'avbussiness': result['avbusiness'], 'aveconomy': result['aveconomy'],'economycost': result['economycost'],'busisnesscost': result['businesscost']}
         data.append(result)
    return data

#Flight Id Search
@app.route('/searchid', methods=['GET', 'POST'])
def searchid():
    if request.method == 'POST':
        id =  request.form.get('id')
        results = flights.find_one({"_id" : id})
        data = []
    for result in results:
       result = { 'from': result['from'], 'to': result['to'],'date':result['date'], 'avbussiness': result['avbusiness'], 'aveconomy': result['aveconomy'],'economycost': result['economycost'],'busisnesscost': result['businesscost']}
       data.append(result)

#Reservation     
@app.route('/reservation', methods=['GET', 'POST'])#
def reservation():
   if request.method == 'POST':
        id =  request.form.get('id')
        existing_flight=flights.find({'_id':id})
        if existing_flight :
          id =random.randint(1, 100)
          username =  request.form.get('username')
          surname =  request.form.get('surname')
          email =  request.form.get('email')
          dateofbirth= request.form.get('dateofbirth')
          passportcode= request.form.get('passportcode')
          fro =existing_flight.get("from")
          to =existing_flight.get("to")
          date=existing_flight.get("date")
          category= request.form.get('from')
          if category=="business":
           flights.update_one("avbusiness", "avbusiness-1")
          elif category=="economy":
           flights.update_one("avbusiness", "aveconomy-1")

        newreservation = {
        '_id':id,
        'username': username,
        'surname': surname,
        'email': email,
        'dateofbirth':dateofbirth,
        'passportcode':passportcode,
        'from':fro,
        'to':to,
        'date':date
    }
        reservations.insert_one(newreservation)

#Show Reservations  
@app.route('/showreservation', methods=['GET', 'POST'])#
def showreservation():   
 if request.method == 'POST':
  response = request.get('http://localhost:5000/login')
  email = response['email']
  existing_reservations=reservations.find({'email':email})
 for i in existing_reservations:
  print(i)     

#Show Elements Of Reservation  
@app.route('/showreservation', methods=['GET', 'POST'])#
def showelements():  
 if request.method == 'POST':
  id = request.form.get('id')
  results = reservations.find({'_id':id})

#Delete  Reservation
@app.route('/deletere', methods=['GET', 'POST'])#
def deletere():
 if request.method == 'POST':
  id = request.form.get('id')
  reservation.delete_one("_id")
  category=flights.get("category")
 if category=="business":
           flights.update_one("avbusiness", "avbusiness-1")
 elif category=="economy":
           flights.update_one("avbusiness", "aveconomy-1")

#Delete User  
@app.route('/deleteus', methods=['GET', 'POST'])#
def deleteus():
 if request.method == 'POST':
  response = request.get('http://localhost:5000/login')
  email=response['email']
  users.delete({'email':email})

#Register
@app.route('/flight', methods=['GET','POST'])
def createflight():
   fro = request.form.get('from')
   to = request.form.get('to')
   date = request.form.get('date')
   avbusiness = request.form.get('avbusiness')
   aveconomy=request.form.get('aveconomy')
   businesscost = request.form.get('businesscost')
   economycost=request.form.get('economycost')

   if not fro or not  to or not avbusiness or not date or not aveconomy: 
    return "Please fill in all the required fields."
   newflight = {
        'from': fro,
        'to': to,
        'date': date,
        'avbusiness': avbusiness,
        'aveconomy':avbusiness,
        'businesscost': businesscost,
        'economycost': economycost
     }
   flights.insert_one(newflight)
   return "Register Succesful"

@app.route('/updatecost', methods=['POST'])
def updatecost():
   response = request.get('http://localhost:5000/login')
   role=response['role']
   newcost1 = request.form.get('newcost1')
   newcost2 = request.form.get('newcost2')
   if role=='admin':
    id = request.form.get('_id')
    myquery = { "_id": id }
    cost1 = { "$set": { "economycost": newcost1 } }
    cost2 ={ "$set": { "businesscost": newcost2 } }
    flights.update_one(myquery,cost1)
    flights.update_one(myquery,cost2)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
