from ..Action import Action
from DB_utils import update_song_nomination, song_nomination_exist
from utils import list_option, get_selection

class ModifySongNomination(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["nomination_name", "ceremony_id"]

    def exec(self, conn):
        """
        Modify a song nomination in the database.
        :param conn: Connection to the client.
        """
        # 讀取提名 ID
        nomination_id = self.read_input(conn, "nomination ID")

        # 確認提名是否存在
        if not song_nomination_exist(nomination_id):
            conn.send(f'\nNomination ID {nomination_id} does not exist!\n'.encode('utf-8'))
            return

        # 提供可修改的欄位選單
        msg = '[INPUT] Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        # 獲取用戶選擇的欄位和新值
        select_item = get_selection(conn, self.options)
        new_value = self.read_input(conn, f'new value for {select_item}')

        # 更新資料庫
        try:
            update_song_nomination(nomination_id, select_item, new_value)
            conn.send(f'\nNomination modified successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to modify nomination: {e}\n'.encode('utf-8'))
