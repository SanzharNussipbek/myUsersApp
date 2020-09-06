import sqlite3

class User:

    # Validate new user's details
    def valid_info(self, user_details: list) -> bool:
        return len(user_details) == 5 and type(user_details[0]) == str and type(user_details[1]) == str and type(user_details[2]) == int and type(user_details[3]) == str and type(user_details[4]) == str
    
    # Check if a user with the given id already exists
    def exists(self, id: int) -> bool:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("""SELECT COUNT(*) 
                                FROM users 
                                WHERE id=%d""" % id)
            conn.commit()
            res = res.fetchone() != 0
            conn.close()
            return res
        except:
            print("Error while executing a query.")
    
    # Get size of the database
    def size(self) -> int:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("SELECT COUNT(*) FROM users")
            conn.commit()
            size = res.fetchone()[0]
            conn.close()
            return size
        except:
            print("Error while executing a query (size).")
            return -1

    # Insert user info into table
    def create(self, user_info: dict) -> int:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("SELECT COUNT(*) FROM users")
            conn.commit()
            for row in res:
                id = row[0]
            
            c.execute("""INSERT INTO users 
                        VALUES (%d, '%s', '%s', '%d', '%s', '%s')""" 
                        % (id, user_info['firstname'], user_info['lastname'], int(user_info['age']), user_info['password'], user_info['email']))
            conn.commit()
            conn.close()
            return id
        except:
            print("Error while executing a query.")
    
    # Get user from table by user id
    def get(self, user_id: int) -> dict:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("""SELECT * 
                                FROM users 
                                WHERE id=%d""" % user_id)
            conn.commit()
            data = res.fetchone()
            if data == None:
                return '>>User with id "%d" does not exist' % user_id
            
            return {
                    'id': data[0],
                    'firstname': data[1],
                    'lastname': data[2],
                    'age': data[3],
                    'password': data[4],
                    'email': data[5],
                }
            conn.close()
        except:
            print("Error while executing a query.")

    
    # Get all entries from the table
    def all(self, password = True) -> list:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            res = c.execute("SELECT * FROM users")
            conn.commit()
            users = []
            for row in res:
                if row == None:
                    return '">>my_user_app" database is empty'
                user = {
                    'id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'age': row[3],
                    'email': row[5],
                }

                if password: user['password'] = row[4]
                users.append(user)
            conn.close()
            return users
        except:
            print("Error while executing a query.")
    
    # Update user's attribute with the given value
    def update(self, user_id: int, attribute: str, value: str or int) -> dict:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            if type(value) == str:
                query = """UPDATE users 
                            SET %s='%s' 
                            WHERE id=%d""" % (attribute, value, user_id)
            else:
                query = """UPDATE users 
                            SET %s=%d 
                            WHERE id=%d""" % (attribute, value, user_id)
            
            c.execute(query)
            conn.commit()
            return self.get(user_id)
        except:
            print("Error while executing a query.")

    # Delete the user from table
    def destroy(self, user_id: int) -> None:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            if not self.exists(user_id):
                print('>>User with id "%d" does not exist' % user_id)
                return
            
            c.execute("""DELETE FROM users 
                            WHERE id=%d""" % user_id)
            conn.commit()
            conn.close()
        except:
            print("Error while executing a query.")

    # Delete all rows in the table
    def destroy_all(self) -> None:
        try:
            conn = sqlite3.connect('my_user_app.db')
            c = conn.cursor()
            c.execute("DELETE FROM users")
            conn.commit()
            conn.close()
        except:
            print("Error while executing a query.")
    
    # Print single user hash
    def print_user(self, user_info: dict) -> None:
        if user_info is None or len(user_info) == 0:
            print('>>Please specify the user')
            return
        
        for key,value in user_info.items():
            print('  ',key,':',value)
        print('\n   ------------------------------------------')

    # Print list of user hashes:
    def print_users(self, users: list) -> None:
        if users is None or len(users) == 0:
            print('>>Please specify the users')
            return

        print("\n>>All users:")
        for user_info in users:
            self.print_user(user_info)

    # Populate the database
    def populate(self) -> None:
        users = [
            {
                "firstname": "Leah",
                "lastname": "Stephens",
                "age": 39,
                "password": "nisi5f525e70c3a8f72a2dea045f",
                "email": "leah.stephens@mail.com"
            },
            {
                "firstname": "Wilkerson",
                "lastname": "Mejia",
                "age": 21,
                "password": "voluptate5f525e707a073b5faa86e3c3",
                "email": "wilkerson.mejia@mail.net"
            },
            {
                "firstname": "Billie",
                "lastname": "Cunningham",
                "age": 36,
                "password": "sint5f52296ccd68714ae12762a7",
                "email": "billie.cunningham@mail.net"
            },
            {
                "firstname": "Carole",
                "lastname": "Morin",
                "age": 20,
                "password": "enim5f52296c5e0306e88a6ddeec",
                "email": "carole.morin@mail.org"
            },
            {
                "firstname": "Vicki",
                "lastname": "Bryan",
                "age": 30,
                "password": "mollit5f52296c6216ec273cc7fd7d",
                "email": "vicki.bryan@mail.ca"
            },
            {
                "firstname": "Newton",
                "lastname": "Mccoy",
                "age": 259,
                "password": "amet5f52296cd4df48e4dcb4604a",
                "email": "newton.mccoy@mail.biz"
            },
            {
                "firstname": "Valentine",
                "lastname": "Knight",
                "age": 32,
                "password": "ad5f52296cb0ad9faf3fb1425a",
                "email": "valentine.knight@mail.co.uk"
            },
            {
                "firstname": "Stout",
                "lastname": "Evans",
                "age": 32,
                "password": "aute5f52296cb01dacad2044024e",
                "email": "stout.evans@mail.biz"
            },
            {
                "firstname": "Addie",
                "lastname": "Giles",
                "age": 22,
                "password": "labore5f52296cde4da6a11f465b3b",
                "email": "addie.giles@mail.name"
            },
            {
                "firstname": "Guzman",
                "lastname": "Mills",
                "age": 32,
                "password": "amet5f52296cae054fc4831b4af0",
                "email": "guzman.mills@mail.tv"
            }
        ]
        for user in users:
            self.create(user)


# Function to test the database
def test():

    # Create User object
    user = User()

    # Clear the database from previous entries (if needed)
    user.destroy_all()

    # # Populate the database
    user.populate()

    # Get the number of users in the database
    print('Size: %d' % user.size())
    
#     # # Print users from the database
#     # user.print_users(user.all())
    
#     # # Print users one by one
#     # print('\n>>All users one by one:')
#     # for id in range(10):
#     #     user.print_user(user.get(id))

#     # # Delete one user from table
#     # user.destroy(2)

#     # # Update user info
#     # print('\n>Update age of user with id = 0:')
#     # user.print_user(user.update(0, 'age', 21))

#     # print('\n>Update first name of user with id = 1:')
#     # user.print_user(user.update(1, 'firstname', 'Sanzhar'))

#     # print('\n>Update last name of user with id = 1:')
#     # user.print_user(user.update(1, 'lastname', 'Nussipbek'))


#     # # Check get() method for invalid input
#     # print(user.get(12))
    
#     # # Check destroy() method for invalid input
#     # user.destroy(12)

#     # # Check print_user() method for invalid inputs
#     # user.print_user({})
#     # user.print_user(None)

#     # # Check print_users() method for invalid inputs
#     # user.print_users([])
#     # user.print_users(None)

if __name__ == "__main__":
    try:
        # Connect to database
        conn = sqlite3.connect('my_user_app.db')

        # Create a cursor
        c = conn.cursor()

        # Create a Table
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            age INTEGER,
            password TEXT,
            email TEXT
        )""")

        # Commit the command
        conn.commit()

        # Close the connection
        conn.close()
    except:
        print("Error while executing a query.")

    # Uncomment the line below to test the database
    # test()