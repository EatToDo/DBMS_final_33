from .HighestVoteSinger import HighestVoteSinger
from .ListVotes import ListVoteResults
from .RemoveVote import RemoveVote
from ..Action import Action
from utils import list_option, get_selection

class ManageVotes(Action):
    def exec(self, conn, user):
        """
        Manage votes: View highest vote singer, List all votes, Remove a vote.
        """
        conn.send(
            "[INPUT] Choose an action:\n"
            "1. View Highest Vote Singer\n"
            "2. List Votes Result for a Ceremony\n"
            "3. Remove a Vote by ID\n---> ".encode('utf-8')
        )
        action = get_selection(conn, ["1", "2", "3"])

        if action == "1":
            HighestVoteSinger("View Highest Vote Singer").exec(conn)
        elif action == "2":
            ListVoteResults("List Votes").exec(conn)
        elif action == "3":
            RemoveVote("Remove Vote").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
