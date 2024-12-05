from .Action import Action
from role.User import User
from DB_utils import db_register_user, username_exist

class SignUp(Action):
    def exec(self, conn):
        print(f'Enter SignUp Action')

        # Read Username
        username = self.read_input(conn, "username")
        print(f"Received username: {username}")
        while username_exist(username):
            conn.send("Username exist, ".encode('utf-8'))
            username = self.read_input(conn, "another username")

        # Read Password
        pwd = self.read_input(conn, "password")
        print(f"Received passward: {pwd}")

        # Read_gender
        gender = self.read_input(conn, "gender (you should enter [Male, Female, Other])", )
        print(f"Received gender: {gender}")

        # Read_birthday
        bdate = self.read_input(conn, "birthday (in YYYY-MM-DD format)")
        print(f"Received birthday: {bdate}")

        # Add to DB
        userid = db_register_user(username, pwd, gender, bdate)
        conn.send(f'----------------------------------------\nSuccessfully create account! Userid = {userid}\n'.encode('utf-8'))

        return User(userid, username, pwd, gender, bdate)