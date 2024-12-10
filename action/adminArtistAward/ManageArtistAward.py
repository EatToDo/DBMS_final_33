from .AddArtistAward import AddArtistAward
from .RemoveArtistAward import RemoveArtistAward
from ..Action import Action
from utils import list_option, get_selection

class ManageArtistAward(Action):
    def exec(self, conn,user):
        """
        Manage song nominations: Add, Modify, Remove.
        """
       
        conn.send("[INPUT] Choose an action:\n1. Add\n2. Remove\n---> ".encode('utf-8'))
        action = get_selection(conn, ["1", "2"])

        if action == "1":
            AddArtistAward("Add Song Award").exec(conn)
        elif action == "2":
            RemoveArtistAward("Remove Song Award").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
                
