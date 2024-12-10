from ..Action import Action
from DB_utils import add_performance, add_performance_artist

class AddPerformance(Action):
    def exec(self, conn):
        """
        Add a new performance and link it to artists.
        :param conn: The connection to the client.
        """
        ceremony_id = self.read_input(conn, "ceremony ID")
        performance_name = self.read_input(conn, "performance name")

        try:
            # 新增表演並取得新表演的 ID
            performance_id = add_performance(ceremony_id, performance_name)
            conn.send(f'\nPerformance added successfully! Performance ID: {performance_id}\n'.encode('utf-8'))

            # 詢問表演歌手並加入到 performance_artists 資料表
            while True:
                artist_id = self.read_input(conn, "artist ID for the performance (or type 'done' to finish)")
                if artist_id.lower() == 'done':
                    break

                try:
                    add_performance_artist(performance_id, artist_id)
                    conn.send(f'\nArtist ID {artist_id} added to performance {performance_id}.\n'.encode('utf-8'))
                except Exception as e:
                    conn.send(f'\nFailed to add artist ID {artist_id} to performance: {e}\n'.encode('utf-8'))

        except Exception as e:
            conn.send(f'\nFailed to add performance: {e}\n'.encode('utf-8'))
