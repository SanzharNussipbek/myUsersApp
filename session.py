# Session class to create a login session with a user

import sqlite3

class Session():

    def loggedIn(self, user_id: int) -> bool:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("""SELECT COUNT(*) 
                                FROM sessions 
                                WHERE user_id=%d""" % user_id)
            conn.commit()
            res = res.fetchone() != 0
            conn.close()
            return res
        
        except:
            print("Error while executing a query.")
            return None

    def sign_in(self, user_id: int):
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            c.execute("INSERT INTO sessions VALUES (%d)" % user_id)
            conn.commit()
            conn.close()
        
        except:
            print("Error while executing a query.")
            return None
    
    def sign_out(self, user_id: int):
        try:
            if not self.loggedIn(user_id):
                return 'The user has already logged out.'

            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            c.execute("DELETE FROM sessions WHERE user_id=%d" % user_id)
            conn.commit()
            conn.close()
        
        except:
            print("Error while executing a query.")
            return None


if __name__ == "__main__":
    try:
        # Connect to database
        conn = sqlite3.connect('my_user_app.db')

        # Create a cursor
        c = conn.cursor()

        # Create a Table
        c.execute("CREATE TABLE IF NOT EXISTS sessions (user_id INTEGER PRIMARY KEY)")

        # Commit the command
        conn.commit()

        # Close the connection
        conn.close()
    except:
        print("Error while executing a query.")