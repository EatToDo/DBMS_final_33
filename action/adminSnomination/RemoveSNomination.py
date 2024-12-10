from ..Action import Action
from DB_utils import remove_song_nomination, song_nomination_exist

class RemoveSongNomination(Action):
    def exec(self, conn):
        """
        Execute the process of removing a song nomination.
        :param conn: The connection to the client.
        """
        # 讀取提名 ID
        nomination_id = self.read_input(conn, "nomination ID")

        # 檢查提名是否存在
        if not song_nomination_exist(nomination_id):
            conn.send(f'\nNomination with ID {nomination_id} does not exist!\n'.encode('utf-8'))
            return

        try:
            # 呼叫刪除提名邏輯
            remove_song_nomination(nomination_id)
            conn.send(f'\nNomination with ID {nomination_id} removed successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove nomination with ID {nomination_id}: {e}\n'.encode('utf-8'))
