from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps, loads
from my_user_model import User
from session import Session

#Create a engine for connecting to SQLite3.
#Assuming my_user_app.db is in your app root folder

e = create_engine('sqlite:///my_user_app.db')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
session = Session()
db = User()

def get_data(request):
    # get data from the request and cut the ends
    data = request.get_data()
    data = str(data)[2:-1]

    # check if data is empty or contains only spaces (meaning that the request is sent with url arguments)
    if len(data) == 0 or data.isspace():
        data = request.args
    
    # if data is not empty, it means that the request is sent with curl or in similar way
    else:

        # check if all arguments were sent separately or with &
        if '&' in data:

            # split the data and turn it into json
            data = data.split('&')
            for i in range(len(data)):
                data[i] = data[i].split('=')

            # create new user's info json from data keys and values
            user_info={}
            for item in data:
                user_info[item[0]] = item[1]
            data = user_info
        
        #if all arguments were sent as a json
        else:
            data = eval(data)
        return data

@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    conn = e.connect()
    
    # GET method
    if request.method == 'GET':
        return make_response({'users': db.all(password=False)})
    
    # POST method
    elif request.method == 'POST':

        # get data from the request
        data = get_data(request)
        
        # create new user and get his id
        new_user_id = db.create(data)

        # return new user's info by getting him by his id
        return make_response(db.get(new_user_id))
    
    elif request.method == 'PUT':

        # check if the user is logged in
        if not session.loggedIn:
            return "Please login to change the password."
        
        # get data from the request
        data = get_data(request)

        # update the user
        user = db.update(data['id'], 'password', data['password'])

        # return the user info
        return make_response(user)
    
    elif request.method == 'DELETE':
        # check if the user is logged in
        if not session.loggedIn:
            return "Please login to delete the user account."
        
        # sign out the user
        session.sign_out()

        # get data from the request
        data = get_data(request)

        # delete the user
        db.destroy(data['id'])

        return "The user was successfully signed out and deleted."

@app.route('/sign_in', methods=['POST'])
def sign_in():
    if request.method == 'POST':
        # get data from the request
        data = get_data(request)

        # get user's id by his email and password
        user_id_email = db.get_id('email', data['email'])
        user_id_password = db.get_id('password', data['password'])

        # set the default message
        msg = "The user was successfully signed in."

        # check if there isn't any user with the given email
        if user_id_email == None:
            msg = "A user with this email does not exist"
        
        # check if there isn't any user with the given email
        elif user_id_password == None:
            msg = "A user with this password does not exist"
        
        # check if the email and password ids do not match
        elif user_id_email != user_id_password:
            msg = "The email or password is not correct. Please try again"
        
        # sign in the user
        else:
            session.sign_in(user_id_email)
        
        return msg

@app.route('/sign_out', methods=['DELETE'])
def sign_out():
    if request.method == 'DELETE':

        # Check if the user is signed in
        if not session.loggedIn:
            return "Please login to sign out"

        # get data from the request
        data = get_data(request)

        # sign out the user
        session.sign_out(data['id'])

        return "The user was successfully signed out."



if __name__ == '__main__':
     app.run(debug=True)