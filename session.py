class Session():
    def __init__(self):
        user_id = None
        loggedIn = False
    
    def sign_in(self, user_id: int) -> None:
        self.user_id = user_id
        self.loggedIn = True

    def sign_out(self) -> None:
        self.user_id = None
        self.loggedIn = False
