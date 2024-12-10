from ..Action import Action
from DB_utils import update_performance, performance_exist, add_performance_artist, remove_performance_artist, get_performance_artists
from utils import list_option, get_selection

class ModifyPerformance(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["ceremony_id", "performance_name", "add_artist", "remove_artist"]

    def exec(self, conn):
        """
        Modify performance details or manage associated artists.
        :param conn: The connection to the client.
        """
        performance_id = self.read_input(conn, "performance ID")

        # 檢查表演是否存在
        if not performance_exist(performance_id):
            conn.send(f'\nPerformance with ID {performance_id} does not exist!\n'.encode('utf-8'))
            return

        # 顯示修改選單
        msg = '[INPUT] What do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))
        select_item = get_selection(conn, self.options)

        try:
            if select_item == "ceremony_id":
                new_value = self.read_input(conn, "new ceremony ID")
                update_performance(performance_id, "ceremony_id", new_value)
                conn.send(f'\nPerformance ceremony ID updated successfully!\n'.encode('utf-8'))

            elif select_item == "performance_name":
                new_value = self.read_input(conn, "new performance name")
                update_performance(performance_id, "performance_name", new_value)
                conn.send(f'\nPerformance name updated successfully!\n'.encode('utf-8'))

            elif select_item == "add_artist":
                artist_id = self.read_input(conn, "artist ID to add to the performance")
                add_performance_artist(performance_id, artist_id)
                conn.send(f'\nArtist ID {artist_id} added to performance {performance_id}.\n'.encode('utf-8'))

            elif select_item == "remove_artist":
                while True:
                    # 獲取當前表演者列表
                    artist_list = get_performance_artists(performance_id)

                    # 如果只剩一位表演者，退出功能
                    if len(artist_list) <= 1:
                        conn.send(f'\nOnly one artist remains. Cannot remove more artists.\nReturning to main menu.\n'.encode('utf-8'))
                        break

                    # 列出表演者並提示輸入
                    artist_list_str = "\n".join([f"Artist ID: {artist_id}" for artist_id in artist_list])
                    conn.send((f"\nCurrent artists in the performance:\n{artist_list_str}\n"
                                ).encode('utf-8'))
                    
                    # 使用者輸入 artist_id 或 done
                    artist_id = self.read_input(conn, " the artist ID to remove or type 'done' to exit")
                    if artist_id.lower() == 'done':
                        break

                    try:
                        artist_id = int(artist_id)  # 驗證輸入是否為數字
                    except ValueError:
                        conn.send(f'\nInvalid input. Please enter a valid artist ID or type "done" to exit.\n'.encode('utf-8'))
                        continue

                    if artist_id not in artist_list:
                        conn.send(f'\nInvalid artist ID: {artist_id}. Please try again or type "done" to exit.\n'.encode('utf-8'))
                        continue

                    # 刪除表演歌手
                    try:
                        remove_performance_artist(performance_id, artist_id)
                        conn.send(f'\nArtist ID {artist_id} removed from performance {performance_id}.\n'.encode('utf-8'))
                    except Exception as e:
                        conn.send(f'\nFailed to remove artist ID {artist_id} due to: {e}\n'.encode('utf-8'))

        except Exception as e:
            conn.send(f'\nFailed to modify performance: {e}\n'.encode('utf-8'))
