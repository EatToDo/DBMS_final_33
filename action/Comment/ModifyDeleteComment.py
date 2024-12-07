from ..Action import Action
from DB_utils import list_your_comment, update_comment, delete_comment
from utils import list_option, get_selection
from tabulate import tabulate

class ModifyDeleteComment(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = ['Modify', 'Delete']

    def exec(self, conn, user):
        print("ModifyDeleteComment")
        userid = user.get_userid()

        conn.send("The following are your comment record.".encode('utf-8'))
        table, print_table = list_your_comment(userid)
        if not table:
            conn.send("No comments found.\n".encode('utf-8'))
            return

        self.send_table(conn, print_table)

        while True:
            conn.send("Please enter the No. of the comment you want to select, or 0 to cancel:".encode('utf-8'))
            try:
                selection = int(self.read_input(conn, ""))
                if selection == 0:
                    conn.send("Operation cancelled.\n".encode('utf-8'))
                    return

                if 1 <= selection <= len(table):
                    selected_comment = table[selection - 1]
                    comment_id, performance_name, comment_text = selected_comment[1:]
                    conn.send(f"You selected:\nPerformance: {performance_name}\nComment: {comment_text}\n".encode('utf-8'))
                    msg = '[INPUT]What do you want to do?\n' + list_option(self.option) + '---> '
                    conn.send(msg.encode('utf-8'))
                    action = get_selection(conn, self.option)
                    if action == 'Modify':
                        comment_text = self.read_input(conn, "new comment text")
                        update_comment(comment_id, userid, comment_text)
                        conn.send(f"[SUCCESS] Comment updated successfully.\n".encode('utf-8'))
                        conn.send(f"New Comment:\nPerformance: {performance_name}\nComment: {comment_text}\n".encode('utf-8'))
                    if action == 'Delete':
                        delete_comment(comment_id)
                        conn.send(f"[SUCCESS] Comment deleted successfully.\n".encode('utf-8'))
                else:
                    conn.send("[INPUT] Invalid No. Please try again.\n".encode('utf-8'))
            except ValueError:
                conn.send("[INPUT] Please enter a valid number.\n".encode('utf-8'))