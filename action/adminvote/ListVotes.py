from DB_utils import fetch_vote_results_for_ceremony
from ..Action import Action

class ListVoteResults(Action):
    def exec(self, conn):
        """
        List the vote counts for each artist in a specific ceremony.
        """
        ceremony_id = self.read_input(conn, "ceremony ID")

        try:
            vote_results = fetch_vote_results_for_ceremony(ceremony_id)
            if not vote_results:
                conn.send(f"\nNo votes found for Ceremony ID {ceremony_id}.\n".encode('utf-8'))
                return

            conn.send(f"\nVote results for Ceremony ID {ceremony_id}:\n".encode('utf-8'))
            for artist_id, name, total_votes in vote_results:
                conn.send(f"- Artist ID: {artist_id}, Name: {name}, Total Votes: {total_votes}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to fetch vote results: {e}\n".encode('utf-8'))
