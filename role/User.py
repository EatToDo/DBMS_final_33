from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.ModifyUserInfo import ModifyUserInfo
from action.Vote.VoteManage import VoteManage
from action.Comment import Comment
from action.ListComment import ListComment
from action.ModifyDeleteComment import ModifyDeleteComment

class User(Role):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)

        self.user_action =  [
                                VoteManage("Add/Modify/Delete/List Vote"),
                                Comment("Comment The Performance"),
                                ListComment("Find Comment"),
                                ModifyDeleteComment("Modify / Delete Your Comment"),
                                ModifyUserInfo("Modify User Info"),
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
