from DB_utils import add_album_nomination
from ..Action import Action

class AddAlbumNomination(Action):
    def exec(self, conn):
        """
        Add a new nomination for an album.
        """
        album_id = self.read_input(conn, "album ID")
        ceremony_id = self.read_input(conn, "ceremony ID")
        award_name = self.read_input(conn, "award name")
        
        try:
            nomination_id = add_album_nomination(album_id=album_id, ceremony_id=ceremony_id, award=award_name)
            conn.send(f"\nNomination added successfully! Nomination ID: {nomination_id}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to add nomination: {e}\n".encode('utf-8'))
