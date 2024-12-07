from ..Action import Action
from DB_utils import fetch_all_ceremony, fetch_performance_ceremony, get_performance_id, list_comment, list_your_comment
from utils import list_option, get_selection

class ListComment(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = fetch_all_ceremony()
        self.action_opt = ['All your comments', 'Comment of specific performances']

    def format_ceremony_id(ceremony_id):
        if 11 <= ceremony_id % 100 <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(ceremony_id % 10, "th")
        return f"{ceremony_id}{suffix}"

    def exec(self, conn, user):
        print("ListComment")
        userid = user.get_userid()
        msg = '[INPUT]What do you want to search?\n' + list_option(self.action_opt) + '---> '
        conn.send(msg.encode('utf-8'))
        action = get_selection(conn, self.action_opt)
        if action == 'All your comments':
            table, print_table = list_your_comment(userid)
            if not table:
                conn.send("No comments found.\n".encode('utf-8'))
                return
            self.send_table(conn, print_table)
            return

        if action == 'Comment of specific performances':
            msg = '[INPUT]The following are all ceremonies\n' + list_option(self.option) + '---> '
            conn.send(msg.encode('utf-8'))

            ceremony_id = get_selection(conn, self.option)
            performance_option = fetch_performance_ceremony(int(ceremony_id))

            msg = '[INPUT]The following are all performances this ceremony\n' + list_option(performance_option) + '---> '
            conn.send(msg.encode('utf-8'))

            selected_performance = get_selection(conn, performance_option)
            artist_name = selected_performance[0]
            performance_name = selected_performance[1]
            conn.send(f"The artist you selected: {artist_name}.The performance you selected : {performance_name}\n".encode('utf-8'))

            performance_id = get_performance_id(ceremony_id, performance_name)
            table_comment = list_comment(performance_id)

            self.send_table(conn, table_comment)
            return