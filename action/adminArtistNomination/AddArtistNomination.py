from DB_utils import add_artist_nomination
from ..Action import Action

class AddArtistNomination(Action):
    def exec(self, conn):
        """
        Add a new nomination for an artist.
        """
        artist_id = self.read_input(conn, "artist ID")
        ceremony_id = self.read_input(conn, "ceremony ID")
        award_name = self.read_input(conn, "award name")
        
        try:
            nomination_id = add_artist_nomination(artist_id=artist_id, ceremony_id=ceremony_id, award=award_name)
            conn.send(f"\nNomination added successfully! Nomination ID: {nomination_id}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to add nomination: {e}\n".encode('utf-8'))
