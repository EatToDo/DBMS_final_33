from ..Action import Action
from utils import list_option, get_selection
from .Comment import Comment
from .ListComment import ListComment
from .ModifyDeleteComment import ModifyDeleteComment

class CommentManage(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [Comment("Comment"),
                        ModifyDeleteComment("Delete / Modify Your Comment"),
                        ListComment("List Records")]

    def exec(self, conn, user):
        print("Comment")

        conn.send("----------------------------------------\n".encode('utf-8'))
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))



        action = get_selection(conn, self.options)
        action.exec(conn, user)
