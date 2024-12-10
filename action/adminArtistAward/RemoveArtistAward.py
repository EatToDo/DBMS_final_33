from DB_utils import remove_artist_award, artist_award_exist
from ..Action import Action

class RemoveArtistAward(Action):
    def exec(self, conn):
        """
        Remove an award for a song.
        """
        award_id = self.read_input(conn, "award ID")

        if not artist_award_exist(award_id):
            conn.send(f'\nAward ID {award_id} does not exist!\n'.encode('utf-8'))
            return

        try:
            remove_artist_award(award_id)
            conn.send(f"\nAward ID {award_id} removed successfully!\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to remove award: {e}\n".encode('utf-8'))
