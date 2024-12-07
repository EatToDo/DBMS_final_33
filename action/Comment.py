from .Action import Action
# from DB_utils import get_max_ceremony_id, list_nominated, vote, list_vote_today

class Comment(Action):
    def exec(self, conn, user):
        print("Comment")
        userid = user.get_userid()
        conn.send("Welcome to the comment system!\n".encode('utf-8'))

