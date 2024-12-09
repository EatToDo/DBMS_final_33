from ..Action import Action
from DB_utils import list_vote, fetch_all_ceremony, list_ceremony_vote, list_nominated
from utils import list_option, get_selection

class ListHistoryVote(Action):

    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = fetch_all_ceremony()
        self.action_opt = ['All your votes', 'Vote of specific ceremony']

    def exec(self, conn, user):
        print("ListHistoryVote")
        userid = user.get_userid()
        conn.send("----------------------------------------\n".encode('utf-8'))
        msg = '[INPUT]What do you want to search?\n' + list_option(self.action_opt) + '---> '
        conn.send(msg.encode('utf-8'))
        action = get_selection(conn, self.action_opt)

        if action == 'All your votes':
            conn.send(f"\nHere are your voting records.\n".encode('utf-8'))
            table_vote, print_table = list_vote(userid)
            if not table_vote:
                conn.send("No voting records found.\n".encode('utf-8'))
                return
            self.send_table(conn, print_table)
            return

        if action == 'Vote of specific ceremony':
            msg = '[INPUT]The following are all ceremonies\n' + list_option(self.option) + '---> '
            conn.send(msg.encode('utf-8'))

            ceremony_id = get_selection(conn, self.option)
            conn.send(f"\nThe artists listed below are nominated for this ceremony.".encode('utf-8'))
            table_artists, opt = list_nominated(ceremony_id)
            self.send_table(conn, table_artists)
            conn.send(f"\nThe following is the record of vote.\n".encode('utf-8'))
            table_ceremony = list_ceremony_vote(ceremony_id)
            self.send_table(conn, table_ceremony)
            return