from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.ModifyUserInfo import ModifyUserInfo
from action.VoteForSinger import VoteForSinger

class User(Role):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)

        self.user_action =  [
                                VoteForSinger("VoteForSinger"),
                                Logout("Logout"),
                                Exit("Leave System"),
                                ModifyUserInfo("ModifyUserInfo")
                            ]
