from DB_utils import add_song_nomination
from ..Action import Action
from utils import get_selection, list_option

class AddSongNomination(Action):
    def exec(self, conn):
        """
        Add a new nomination for a song.
        """
        
        song_id = self.read_input(conn, "song ID")
    
        ceremony_id = self.read_input(conn, "ceremony ID")
     
        award_name = self.read_input(conn, "award name")
        
        try:
            nomination_id = add_song_nomination(song_id=song_id, ceremony_id=ceremony_id, award=award_name)
            conn.send(f"\nNomination added successfully! Nomination ID: {nomination_id}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to add nomination: {e}\n".encode('utf-8'))
