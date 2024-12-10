from ..Action import Action
from DB_utils import append_song



class AddSong(Action):
    def exec(self, conn):
        title = self.read_input(conn, "song title")  # 修正欄位名稱
        release_year = self.read_input(conn, "release year (YYYY)")  # 修正欄位名稱
        album_id = self.read_input(conn, "album ID")

        try:
            song_id = append_song(title, release_year, album_id)
            conn.send(f'\nSong added successfully! Song ID: {song_id}\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to add song: {e}\n'.encode('utf-8'))
