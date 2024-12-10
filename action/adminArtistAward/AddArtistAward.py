from DB_utils import add_artist_award
from ..Action import Action

class AddArtistAward(Action):
    def exec(self, conn):
        """
        Add a new award for a artist.
        """
        nomination_id = self.read_input(conn, "nomination ID")

        
        try:
            award_id = add_artist_award(nomination_id= nomination_id)
            conn.send(f"\nAward added successfully! Award ID: {award_id}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to add award: {e}\n".encode('utf-8'))
