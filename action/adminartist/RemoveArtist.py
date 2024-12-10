from ..Action import Action
from DB_utils import remove_artist, artist_exist

class RemoveArtist(Action):
    def exec(self, conn):
        """
        Execute the process of removing an artist and all related records.
        :param conn: The connection to the client.
        """
        artist_id = self.read_input(conn, "artist ID")

        # 檢查歌手是否存在
        if not artist_exist(artist_id):
            conn.send(f'\nArtist with ID {artist_id} does not exist!\n'.encode('utf-8'))
            return

        try:
            # 呼叫刪除歌手邏輯
            remove_artist(artist_id)
            conn.send(f'\nArtist with ID {artist_id} and all related records removed successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove artist with ID {artist_id}: {e}\n'.encode('utf-8'))
