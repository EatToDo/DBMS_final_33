from ..Action import Action
from DB_utils import song_exist, remove_song

class RemoveSong(Action):
    def exec(self, conn):
        song_id = self.read_input(conn, "song ID")

        if not song_exist(song_id):
            conn.send(f'\nSong does not exist!\n'.encode('utf-8'))
            return

        try:
            # 調用更新後的 remove_song 函數
            remove_song(song_id)
            conn.send(f'\nSong and related records removed successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove song: {e}\n'.encode('utf-8'))
