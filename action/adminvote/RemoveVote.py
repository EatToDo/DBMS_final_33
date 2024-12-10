from DB_utils import remove_vote, vote_exist
from ..Action import Action

class RemoveVote(Action):
    def exec(self, conn):
        """
        Remove a specific vote by ID.
        """
        vote_id = self.read_input(conn, "vote ID")

        if not vote_exist(vote_id):
            conn.send(f"\nVote ID {vote_id} does not exist!\n".encode('utf-8'))
            return

        try:
            remove_vote(vote_id)
            conn.send(f"\nVote ID {vote_id} removed successfully.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to remove vote: {e}\n".encode('utf-8'))
