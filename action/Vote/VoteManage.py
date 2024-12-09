from ..Action import Action
from utils import list_option, get_selection
from .DeleteYourVote import DeleteYourVote
from .ListHistoryVote import ListHistoryVote
from .VoteAndModify import VoteAndModify

class VoteManage(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [VoteAndModify("Add/Modify Vote"),
                        DeleteYourVote("Delete your vote"),
                        ListHistoryVote("List your voting records")]

    def exec(self, conn, user):
        print("Vote")

        conn.send("----------------------------------------\n".encode('utf-8'))
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))



        action = get_selection(conn, self.options)
        action.exec(conn, user)
