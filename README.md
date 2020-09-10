# My Users App

This project is made as a part of studying in [Qwant.kz](http://qwant.kz) & Qwasar Silicon Valley Coding school. It is an implementation of **RESTFul API** using **Python, Flask, SQLite3** and **SQLAlchemy** for Back-End, with simple UI using Bootstrap 4 for the Front-End of the system. 

## How to run the project:

To run the project, we first need to install required libraries. To do that, in Docode terminal, type: 

```bash
pip install flask sqlalchemy
```

After that, we need to run the [app.py](http://app.py) file with the following command in terminal: 

```bash
python app.py
```

Then, you can go to [`http://localhost:5000/`](http://web-xxxxxxxxx.docode.qwasar.io/) and you should see:

![ScreenShot](/screenshots/homePage.png)

When you click on 'Go to Users', you will redirected to /users route:

![ScreenShot](/screenshots/usersPage.png)

If you click on 'Sign in' button at the top, you will go to login page:

![ScreenShot](/screenshots/loginPage.png)

After you login, you can go back to /users page and see that 'Sign in' button turned into 'My Profile' button. By clicking on it, you will see your profile page. You can also click on any user in the table and see his/her profile:

![ScreenShot](/screenshots/profilePage.png)

## The web-app consists of several dependancies in different files:

1. `my_user_model.py`

    This file contains User class for handling INSERT, SELECT, DELETE, UPDATE results into SQLite3 database named my_user_app.db.

    **User class** has the following methods:

    - `def create(user_info)`
        - It will create a user. User info will be: `firstname`, `lastname`, `age`, `password` and `email` And it will return a unique ID (a positive `integer`)
    - `def get(user_id)`
        - It will retrieve the associated `user` and return all information contained in the database.
    - `def all()`
        - It will retrieve all users and return a hash of users.
    - `def update(user_id, attribute, value)`
        - It will retrieve the associated `user`, update the attribute send as `parameter` with the `value` and return the user `hash`.
    - `def destroy(user_id)`
        - It will retrieve the associated `user` and destroy it from your database.
    - `def destroy_all()`
        - It will  destroy all user entries in the database
    - `def size()`
        - Get number of users in the database
    - `def exists(user_id)`
        - Check if a user with the given id already exists
    - `def valid_info(user_info)`
        - Validate new user's details
    - `def get_id(attribute, value)`
        - Get id of the user by his attribute and its value
    - `def print_user(user_info)`
        - Print single user hash
    - `def print_users(users)`
        - Print list of user hashes
    - `def populate()`
        - Populate the database with mock data
2. `session.py`

    This file contains Session class for managing **login session** of a user. Session object has two attributes: `user_id` and `loggedIn`

    **Session class** has the following methods:

    - `def __init__()`
        - Create an instance of the class
        - Set the initial values of the `user_id` and `loggedIn` variables to `None` and `False` respectively
    - `def sign_in(user_id)`
        - Set the `user_id` of the Session object to the `given one`
        - Set the `loggedIn` variable to `True`
    - `def sign_out()`
        - Set the variables to their initial state
3. `app.py`

    This is a min file which has to be run for the system to start working. It establishes a connection with the `my_user_app` database, `User` and `Session` classes.

    It has five routes:

    1. `'/'`
        - Home route. It will welcome the user and ask to go to the `/users` route
    2. `/users`
        - Route with four methods: GET, POST, PUT and DELETE
        - **GET**: This action will return all users (without their passwords).
        - **POST**: Receiving `firstname`, `lastname`, `age`, `password` and `email`. It will create a user and store in your database.
        - **PUT**: This action require a user to be `logged in`. It will receive a new password and will update it. It returns the hash of the user.
        - **DELETE**: This action require a user to be `logged in`. It will sign_out the current user and it will destroy the current user.
    3. `/users/id`
        - Route to get a single user with the only **GET** method
    4. `/sign_in` 
        - Route to sign in the user into the system: GET and POST requests
        - **GET**: returns a login page template
        - **POST**: Receiving `email` and `password`. It will add a session containing the `user_id` in order to be `logged in`.
    5. `/sign_out` 
        - Route to sign out the user from the system: **DELETE** method wrapped in **POST**
        - Since HTML forms does not support any other methods than GET and POST, in this project PUT and DELETE methods are wrapped inside the POST form with the following trick in .html file:

            ```html
            <input type="hidden" name="_method" value="DELETE">
            or 
            <input type="hidden" name="_method" value="PUT">
            ```

        - **DELETE**: This action require a user to be `logged in`. It will sign_out the current user.

    4. `views` directory

    - This directory stores templates for rendering:
        1. `home.html`: for **'/'** route to welcome the user
        2. `index.html`: for **/users** route with the table of users and forms for all the actions
        3. `login.html`: for **/sign_in** route
        4. `profile.html`: for **/users/id** route to show the user profile details