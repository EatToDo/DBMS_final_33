from .Role import Role
from action.Exit import Exit
from action.Logout import Logout

class User(Role):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)

        self.user_action =  [
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
