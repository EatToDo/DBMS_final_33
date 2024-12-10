from ..Action import Action
from DB_utils import append_artist

class AddArtist(Action):
    def exec(self, conn):
        name = self.read_input(conn, "artist name")
        gender = self.read_input(conn, "artist gender")
        bdate = self.read_input(conn, "artist birthdate (YYYY-MM-DD)")

        try:
            artist_id = append_artist(name, gender, bdate)
            conn.send(f'\nArtist added successfully! Artist ID: {artist_id}\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to add artist: {e}\n'.encode('utf-8'))
