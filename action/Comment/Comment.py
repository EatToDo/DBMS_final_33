from ..Action import Action
from DB_utils import fetch_all_ceremony, fetch_performance_ceremony, get_performance_id, comment
from utils import list_option, get_selection

class Comment(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = fetch_all_ceremony()

    @staticmethod
    def format_ceremony_id(ceremony_id):
        if 11 <= ceremony_id % 100 <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(ceremony_id % 10, "th")
        return f"{ceremony_id}{suffix}"

    def exec(self, conn, user):
        print("Comment")
        userid = user.get_userid()
        conn.send("\n========================================================\n".encode('utf-8'))
        conn.send("Welcome to the comment system!\n\n".encode('utf-8'))

        msg = '[INPUT]Please select a ceremony.\n' + list_option(self.option) + '---> '
        conn.send(msg.encode('utf-8'))

        ceremony_id = get_selection(conn, self.option)
        format_ceremony = self.format_ceremony_id(int(ceremony_id))
        conn.send(f"\nYou selected: {format_ceremony} ceremony\n\n".encode('utf-8'))
        performance_option = fetch_performance_ceremony(int(ceremony_id))

        msg = '[INPUT]The following are all the performances in this ceremony.\n' + list_option(performance_option) + '---> '
        conn.send(msg.encode('utf-8'))

        selected_performance = get_selection(conn, performance_option)
        artist_name = selected_performance[0]
        performance_name = selected_performance[1]
        conn.send(f"\nThe artist you selected: {artist_name}.The performance you selected : {performance_name}\n\n".encode('utf-8'))

        performance_id = get_performance_id(ceremony_id, performance_name)
        c = self.read_input(conn, 'your comment')
        comment(performance_id, userid, c)
        conn.send(f"\nYour comment: {c} recorded successfully!".encode('utf-8'))
        return
