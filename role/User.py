from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.ModifyUserInfo import ModifyUserInfo
# from action.Vote.VoteAndModify import VoteAndModify
# from action.Vote.DeleteYourVote import DeleteYourVote
# from action.Vote.ListHistoryVote import ListHistoryVote
from action.Vote.VoteManage import VoteManage
from action.Comment import Comment
from action.ListComment import ListComment

class User(Role):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(userid, username, pwd, gender, bdate)

        self.user_action =  [
                                VoteManage("Add/Modify/Delete/List Vote"),
                                Comment("Comment the performance"),
                                ListComment("Find Comment"),
                                ModifyUserInfo("Modify User Info"),
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
