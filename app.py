from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps, loads
from my_user_model import User

#Create a engine for connecting to SQLite3.
#Assuming my_user_app.db is in your app root folder

e = create_engine('sqlite:///my_user_app.db')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    conn = e.connect()
    db = User()
    
    # GET method
    if request.method == 'GET':
        return make_response({'users': db.all(password=False)})
    
    # POST method
    elif request.method == 'POST':

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
        
        # create new user and get his id
        new_user_id = db.create(data)

        # return new user's info by getting him by his id
        return make_response(db.get(new_user_id))
    
    elif request.method == 'PUT':
        return 'PUT method'
    
    elif request.method == 'DELETE':
        return 'DELETE method'
    
    else:
        return 'Hello World!'


if __name__ == '__main__':
     app.run(debug=True)