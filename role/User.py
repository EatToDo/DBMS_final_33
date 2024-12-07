from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.ModifyUserInfo import ModifyUserInfo
from action.Vote.VoteManage import VoteManage
from action.Comment.CommentMange import CommentManage

class User(Role):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)

        self.user_action =  [
                                VoteManage("Add/Modify/Delete/List Vote"),
                                CommentManage("Add/Modify/Delete/List Comment"),
                                ModifyUserInfo("Modify User Info"),
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
