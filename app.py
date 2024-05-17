from flask import Flask, url_for, redirect, request, render_template, session, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
from utils.user import User

app=Flask(__name__)

load_dotenv('.env')
app.secret_key=os.getenv('APP_SECRECT_KEY')
user=User(app=app)



@app.route('/login', methods=['GET', 'POST'])
def login():
    emailAddress = str(request.args['emailAddress'])
    password = str(request.args['password'])
    
    status, user_=user.logInUser(emailAddress=emailAddress, password=password)
    
    if status == "Login successful":
        response={"status": status, 'username': user_['username']}
        
    elif status == "Incorrect password":
        response={"status": status, 'username': None}
        
    elif status == "User not found":
        response={"status": status, 'username': None}
        
        
    return jsonify({"response": response})

    
@app.route("/sign-up", methods=['GET', 'POST'])
def signUp():
    username = str(request.args['username'])
    emailAddress = str(request.args['emailAddress'])
    phoneNumber = str(request.args['phoneNumber'])
    password = str(request.args['password'])
        
    status=user.addUser(username=username, emailAddress=emailAddress, phoneNumber=phoneNumber, password=password)
    
    if status:
        session['loggedIn'] = True
        session['emailAddress'] = emailAddress
        session['username']=username
        
        response={"status": "success", 'username': username}
        
    else:
        response={"status": "unsuccess", 'username': None}

    return jsonify({"response" : response})


@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop('loggedIn', None)
    session.pop('emailAddress', None)
    session.pop('username', None)
    
    response={"status": "success"}
    
    return jsonify({"response" : response})
            
if __name__=="__main__":
    app.run(debug=True, port=8000)