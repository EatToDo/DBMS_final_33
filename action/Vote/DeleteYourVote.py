from ..Action import Action
from DB_utils import list_validvote_today, delete_vote, get_max_ceremony_id


class DeleteYourVote(Action):

    def exec(self, conn, user):
        print("DeleteYourVote")
        ceremony_id = get_max_ceremony_id()
        userid = user.get_userid()
        conn.send(f"\nHere are your voting records today.\n".encode('utf-8'))
        table_vote, result = list_validvote_today(userid)
        # if not table_vote:
        #     conn.send("You have no valid votes for today.\n".encode('utf-8'))
        #     return
        self.send_table(conn, table_vote)

        recv = self.read_input(conn, "Do you really want to delete it? (Yes/No, or type any other to back)")
        if recv.lower() == "yes":
            delete_vote(userid, ceremony_id)
            conn.send("Your votes have been deleted successfully.\n".encode('utf-8'))
        elif recv.lower() == "no":
            conn.send("Your votes remain unchanged.\n".encode('utf-8'))
        else:
            conn.send("Returning to the previous menu...\n".encode('utf-8'))
            return

