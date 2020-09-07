# Session class to create a login session with a user

class Session():

    # Create an instance of the class
    # Set the initial values of the user_id and loggedIn variables to None and False
    def __init__(self):
        self.user_id = None
        self.loggedIn = False
    
    # Set the user_id of the Session object to the given one
    # Set the loggedIn variable to True
    def sign_in(self, user_id: int) -> None:
        self.user_id = user_id
        self.loggedIn = True

    # Set the variables to their initial state
    def sign_out(self) -> None:
        self.user_id = None
        self.loggedIn = False
