from ..Action import Action
from DB_utils import remove_artist_nomination, artist_nomination_exist

class RemoveArtistNomination(Action):
    def exec(self, conn):
        """
        Remove an artist nomination.
        """
        nomination_id = self.read_input(conn, "nomination ID")

        if not artist_nomination_exist(nomination_id):
            conn.send(f'\nNomination with ID {nomination_id} does not exist!\n'.encode('utf-8'))
            return

        try:
            remove_artist_nomination(nomination_id)
            conn.send(f'\nNomination with ID {nomination_id} removed successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove nomination: {e}\n'.encode('utf-8'))
