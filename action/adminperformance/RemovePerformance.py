from ..Action import Action
from DB_utils import remove_performance

class RemovePerformance(Action):
    def exec(self, conn):
        """
        Remove a performance and all related artists from the database.
        :param conn: The connection to the client.
        """
        performance_id = self.read_input(conn, "performance ID")

        try:
            # 刪除表演及相關資料
            remove_performance(performance_id)
            conn.send(f'\nPerformance ID {performance_id} and all related artists removed successfully.\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to remove performance: {e}\n'.encode('utf-8'))
