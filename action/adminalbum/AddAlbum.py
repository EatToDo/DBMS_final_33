from ..Action import Action
from DB_utils import append_album

class AddAlbum(Action):
    def exec(self, conn):
        title = self.read_input(conn, "album title")
        release_year = self.read_input(conn, "release year (YYYY)")
        artist_id = self.read_input(conn, "artist ID")

        try:
            album_id = append_album(title, release_year, artist_id)
            conn.send(f'\nAlbum added successfully! Album ID: {album_id}\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to add album: {e}\n'.encode('utf-8'))
