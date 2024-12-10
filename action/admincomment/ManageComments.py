from .ViewComments import ViewComments
from .RemoveComments import RemoveComment
from ..Action import Action
from utils import list_option, get_selection

class ManageComments(Action):
    def exec(self, conn, user):
        """
        Manage comments: View and Remove.
        """
        conn.send(
            "[INPUT] Choose an action:\n"
            "1. View Comments for a Performance\n"
            "2. Remove a Comment by ID\n---> ".encode('utf-8')
        )
        action = get_selection(conn, ["1", "2"])

        if action == "1":
            # 查看特定 performance 的留言
            ViewComments("View Comments").exec(conn)
        elif action == "2":
            # 刪除留言
            RemoveComment("Remove Comment").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
