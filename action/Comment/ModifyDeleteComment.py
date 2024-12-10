from ..Action import Action
from DB_utils import list_your_comment, update_comment, delete_comment, get_lock
from utils import list_option, get_selection
from tabulate import tabulate

class ModifyDeleteComment(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = ['Modify', 'Delete']

    def exec(self, conn, user):
        print("ModifyDeleteComment")
        userid = user.get_userid()

        conn.send(f"\nHere are your comment records.\n".encode('utf-8'))
        table, print_table = list_your_comment(userid)
        if not table:
            conn.send("No comments found.\n".encode('utf-8'))
            return

        self.send_table(conn, print_table)

        conn.send("\n".encode('utf-8'))
        try:
            selection = int(self.read_input(conn, "the No. of the comment you want to select, or 0 to cancel"))
            if selection == 0:
                conn.send("Operation cancelled.\n".encode('utf-8'))
                return

            if 1 <= selection <= len(table):
                selected_comment = table[selection - 1]
                comment_id, performance_name, comment_text = selected_comment[1:]
                conn.send(f"\nYou selected:\nPerformance: {performance_name}\nComment: {comment_text}\n\n".encode('utf-8'))
                msg = '[INPUT]What do you want to do?\n' + list_option(self.option) + '---> '
                conn.send(msg.encode('utf-8'))
                action = get_selection(conn, self.option)

                lock = get_lock(comment_id)
                if not lock.acquire(blocking=False):
                    conn.send("\n[INFO] Another operation is in progress on this comment. Please wait...\n".encode('utf-8'))
                    lock.acquire()

                try:
                    if action == 'Modify':
                        conn.send("\n".encode('utf-8'))
                        comment_text = self.read_input(conn, "new comment text")
                        try:
                            update_comment(comment_id, userid, comment_text)
                            conn.send(f"\n[SUCCESS] Comment updated successfully.\n".encode('utf-8'))
                            conn.send(f"New Comment:\nPerformance: {performance_name}\nComment: {comment_text}".encode('utf-8'))
                        except Exception as e:
                            conn.send(f"\n[ERROR] Failed to update comment: {e}\n".encode('utf-8'))
                    elif action == 'Delete':
                        try:
                            delete_comment(comment_id)
                            conn.send(f"\n[SUCCESS] Comment deleted successfully.\n".encode('utf-8'))
                        except Exception as e:
                            conn.send(f"\n[ERROR] Failed to delete comment: {e}\n".encode('utf-8'))
                finally:
                    lock.release()
            else:
                conn.send("\n[INPUT] Invalid No. Please try again.".encode('utf-8'))
        except ValueError:
            conn.send("\n[INPUT] Please enter a valid number.".encode('utf-8'))