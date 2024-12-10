from DB_utils import fetch_performance_comments
from ..Action import Action

class ViewComments(Action):
    def exec(self, conn):
        """
        View comments for a specific performance.
        """
        performance_id = self.read_input(conn, "performance ID")
        
        try:
            comments = fetch_performance_comments(performance_id)
            if not comments:
                conn.send(f"\nNo comments found for performance ID {performance_id}.\n".encode('utf-8'))
                return
            
            conn.send(f"\nComments for Performance ID {performance_id}:\n".encode('utf-8'))
            for comment_id, content, user_id in comments:
                conn.send(f"- Comment ID: {comment_id}, User ID: {user_id}, Content: {content}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to fetch comments: {e}\n".encode('utf-8'))
