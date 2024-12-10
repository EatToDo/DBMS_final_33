from DB_utils import remove_comment, comment_exist
from ..Action import Action

class RemoveComment(Action):
    def exec(self, conn):
        """
        Remove a specific comment by ID.
        """
        comment_id = self.read_input(conn, "comment ID")

        # 檢查 comment 是否存在
        if not comment_exist(comment_id):
            conn.send(f"\nComment ID {comment_id} does not exist!\n".encode('utf-8'))
            return

        try:
            # 呼叫刪除函數
            remove_comment(comment_id)
            conn.send(f"\nComment ID {comment_id} removed successfully.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to remove comment: {e}\n".encode('utf-8'))
