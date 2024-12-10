from ..Action import Action
from DB_utils import album_exist, remove_album

class RemoveAlbum(Action):
    def exec(self, conn):
        """
        Execute the album removal process.
        :param conn: The connection to the client.
        """
        album_id = self.read_input(conn, "album ID")

        # 檢查專輯是否存在
        if not album_exist(album_id):
            conn.send(f'\nAlbum with ID {album_id} does not exist!\n'.encode('utf-8'))
            return

        try:
            # 呼叫刪除專輯函數
            remove_album(album_id)
            conn.send(f'\nAlbum with ID {album_id} and related records removed successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove album with ID {album_id}: {e}\n'.encode('utf-8'))
