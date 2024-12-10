from .AddSNomination import AddSongNomination
from .ModifySNomination import ModifySongNomination
from .RemoveSNomination import RemoveSongNomination
from ..Action import Action
from utils import list_option, get_selection

class ManageSongNominations(Action):
    def exec(self, conn,user):
        """
        Manage song nominations: Add, Modify, Remove.
        """
       
        conn.send("[INPUT] Choose an action:\n1. Add\n2. Modify\n3. Remove\n---> ".encode('utf-8'))
        action = get_selection(conn, ["1", "2", "3"])

        if action == "1":
            AddSongNomination("Add Song Nomination").exec(conn)
        elif action == "2":
            ModifySongNomination("Modify Song Nomination").exec(conn)
        elif action == "3":
            RemoveSongNomination("Remove Song Nomination").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
                
