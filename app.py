from flask import Flask, request, make_response, render_template
from sqlalchemy import create_engine
from my_user_model import User
from session import Session


# Create an engine for connecting to SQLite3.
# Assuming my_user_app.db is in your app root folder
e = create_engine('sqlite:///my_user_app.db')

# Create a Flask app with the given name and with template folders set to 'views' folder
app = Flask(__name__, template_folder='views')

# Do not sort the response hash keys
app.config['JSON_SORT_KEYS'] = False

# Create the instances of User model and Session class
session = Session()
db = User()

# Template for empty response in template rendering
EMPTY_RESPONSE = {'text':'', 'id':''}


# Process the request and get the needed data from it
def get_data(request):

    # check if the request was made from an HTML form
    if request.form:
        return request.form

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


# Check if hidden method is DELETE wrapped in POST method
def method_is_delete(request):
    '''Workaround for a lack of delete method in the HTML spec for forms.'''
    return request.form.get('_method') == 'DELETE'

# Check if hidden method is PUT wrapped in POST method
def method_is_put(request):
    '''Workaround for a lack of delete method in the HTML spec for forms.'''
    return request.form.get('_method') == 'PUT'

# Function for DELETE request
def users_delete_request(request):
    # check if the user is logged in
    if not session.loggedIn:
        return render_template("index.html", 
                                data = db.all(password=False), 
                                sign_out_delete = {'msg': "Please login to delete the user account.", 'color': 'danger'}, 
                                auth = 'Sign in', 
                                profile = EMPTY_RESPONSE,
                                update = EMPTY_RESPONSE,
                                sign_out = EMPTY_RESPONSE
                            )

    # delete the user
    db.destroy(session.user_id)

    # sign out the user
    session.sign_out()

    return render_template("index.html", 
                            data = db.all(password=False), 
                            sign_out_delete = {'msg': "The user was successfully signed out and deleted.", 'color': 'success'}, 
                            auth = 'Sign in',
                            profile = EMPTY_RESPONSE,
                            update = EMPTY_RESPONSE,
                            sign_out = EMPTY_RESPONSE,
                        )

# Function for PUT request
def users_put_request(request):
    # check if the user is logged in
    if not session.loggedIn:
        return render_template("index.html", 
                                data = db.all(password=False), 
                                update = {'msg': "Please login to change the password", 'color': 'danger'}, 
                                auth = 'Sign in', 
                                profile = EMPTY_RESPONSE,
                                sign_out_delete = EMPTY_RESPONSE,
                                sign_out = EMPTY_RESPONSE,
                            )
    
    # get data from the request
    data = get_data(request)

    # update the user
    user = db.update(session.user_id, 'password', data['password'])
    
    # return the user info
    # return make_response(user)

    return render_template("index.html", 
                            data = db.all(password=False), 
                            update={'msg': "Password successully changed", 'color': 'success'}, 
                            auth='', 
                            profile = {'text': 'My Profile', 'id': session.user_id},
                            sign_out_delete = EMPTY_RESPONSE,
                            sign_out = EMPTY_RESPONSE
                        )


# default route
@app.route('/')
def welcome():
    return render_template("home.html")


# /users route with REST API
@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():

    # Establish a connection with the database engine
    conn = e.connect()
    
    # GET method: return the list with all the users
    if request.method == 'GET':
        # Render the template with the table and pass the data
        auth = 'Sign in' if not session.loggedIn else ''
        
        profile = {
            'text': 'My Profile' if session.loggedIn else '',
            'id' : session.user_id if session.loggedIn else ''
        }
        
        return render_template( "index.html", 
                                data = db.all(password=False), 
                                auth = auth, 
                                profile = profile, 
                                update = EMPTY_RESPONSE,
                                sign_out_delete = EMPTY_RESPONSE,
                                sign_out = EMPTY_RESPONSE
                            )
    
    # POST method: create a new user
    elif request.method == 'POST':

        # Check if there are any hidden methods
        if method_is_delete(request):
            return users_delete_request(request)
        
        elif method_is_put(request):
            return users_put_request(request)

        # get data from the request
        data = get_data(request)

        # create new user and get his id and info
        new_user_id = db.create(data)
        user = db.get(new_user_id)

        # return new user's info by getting him by his id
        # return make_response(user)

        auth = 'Sign in' if not session.loggedIn else ''
        profile = {
            'text': 'My Profile' if session.loggedIn else '',
            'id' : session.user_id if session.loggedIn else ''
        }
        return render_template("index.html", 
                                data = db.all(password=False), 
                                auth = auth, 
                                profile = profile,
                                update = EMPTY_RESPONSE,
                                sign_out_delete = EMPTY_RESPONSE,
                                sign_out = EMPTY_RESPONSE
                            )
    
    # PUT method: update the password of the user who is already logged in
    elif request.method == 'PUT':
        return users_put_request(request)
    
    # DELETE method: sign out the user and delete him from the table
    elif request.method == 'DELETE':
        return users_delete_request(request)


# /sign_in route
@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():

    # POST method: sign in the user
    if request.method == 'POST':

        # get data from the request
        data = get_data(request)

        # get user's id by his email and password
        user_id_email = db.get_id('email', data['email'])
        user_id_password = db.get_id('password', data['password'])

        if session.loggedIn and session.user_id == user_id_email:
            return "This user is already logged in.\n"

        # set the default message
        response = ["The user was successfully signed in.\n","success"]

        # check if there isn't any user with the given email
        if user_id_email == None:
            response = ["A user with this email does not exist.\n", "danger"]
        
        # check if there isn't any user with the given email
        elif user_id_password == None:
            response = ["A user with this password does not exist.\n", "danger"]
        
        # check if the email and password ids do not match
        elif user_id_email != user_id_password:
            response = ["The email or password is not correct. Please try again.\n", "danger"]
        
        # sign in the user
        else:
            session.sign_in(user_id_email)
        
        return render_template("login.html", response = response[0], color=response[1])

    # GET method: login form
    elif request.method == 'GET':
        return render_template("login.html")


# /sign_out route
@app.route('/sign_out', methods=['POST', 'GET'])
def sign_out():

    # DELETE method: sign out the user
    if request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            # Check if the user is signed in
            if not session.loggedIn:
                return render_template("index.html", 
                                        data = db.all(password=False), 
                                        auth = "Sign in", 
                                        profile = EMPTY_RESPONSE,
                                        sign_out = {'msg': "Please login to sign out.", 'color': 'danger'},
                                        update = EMPTY_RESPONSE,
                                        sign_out_delete = EMPTY_RESPONSE
                                    )

            # sign out the user
            session.sign_out()

            return render_template("index.html", 
                                    data = db.all(password=False), 
                                    auth = "Sign in", 
                                    profile = EMPTY_RESPONSE,
                                    sign_out = {'msg':"The user was successfully signed out and deleted", 'color':'success'},
                                    update = EMPTY_RESPONSE,
                                    sign_out_delete = EMPTY_RESPONSE,
                                )
        return 'Invalid method'

    # GET method: get the information of the session
    elif request.method == 'GET':
        # get the value of loggedIn from the session
        response = {'loggedIn' : session.loggedIn}

        # get the user if he is logged in
        if session.loggedIn:
            response['user'] = db.get(session.user_id)
        
        return make_response(response)


# /users/:user_id route for profile page
@app.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    return render_template("profile.html", user = db.get(user_id))
    

# main function to run the app
if __name__ == '__main__':
     app.run(debug=True)