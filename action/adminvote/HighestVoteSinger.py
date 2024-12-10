from DB_utils import fetch_highest_vote_singer
from ..Action import Action

class HighestVoteSinger(Action):
    def exec(self, conn):
        """
        View the highest vote singer for a specific ceremony.
        """
        ceremony_id = self.read_input(conn, "ceremony ID")

        try:
            result = fetch_highest_vote_singer(ceremony_id)
            if not result:
                conn.send(f"\nNo votes found for Ceremony ID {ceremony_id}.\n".encode('utf-8'))
                return

            artist_id, name, total_votes = result
            conn.send(f"\nHighest vote singer for Ceremony ID {ceremony_id}:\n".encode('utf-8'))
            conn.send(f"- Artist ID: {artist_id}, Name: {name}, Total Votes: {total_votes}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to fetch highest vote singer: {e}\n".encode('utf-8'))
