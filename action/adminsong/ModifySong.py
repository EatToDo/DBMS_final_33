from ..Action import Action
from DB_utils import update_song, song_exist
from utils import list_option, get_selection

class ModifySong(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        # 正確的欄位名稱
        self.options = ["title", "release_year", "album_id"]

    def exec(self, conn):
        # 提示用戶輸入 song_id
        song_id = self.read_input(conn, "song ID")

        # 驗證 song_id 是否存在
        if not song_exist(song_id):
            conn.send(f'\nSong with ID {song_id} does not exist!\n'.encode('utf-8'))
            return

        # 提供可修改的欄位選擇
        msg = '[INPUT]Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))
        select_item = get_selection(conn, self.options)

        # 提示輸入新值
        new_value = self.read_input(conn, f'new value for {select_item}')

        # 嘗試更新資料庫
        try:
            update_song(song_id, select_item, new_value)
            conn.send(f'\nSong with ID {song_id} updated successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to modify song: {e}\n'.encode('utf-8'))
