from ..Action import Action
from DB_utils import list_vote

class ListHistoryVote(Action):

    def exec(self, conn, user):
        print("ListHistoryVote")
        userid = user.get_userid()
        conn.send(f"\nBelow are your voting record.\n".encode('utf-8'))
        table_vote = list_vote(userid)

        self.send_table(conn, table_vote)

