from .AddArtistNomination import AddArtistNomination
from .ModifyArtistNomination import ModifyArtistNomination
from .RemoveArtistNomination import RemoveArtistNomination
from ..Action import Action
from utils import list_option, get_selection

class ManageArtistNominations(Action):
    def exec(self, conn, user):
        """
        Manage artist nominations: Add, Modify, Remove.
        """
        conn.send("[INPUT] Choose an action:\n1. Add\n2. Modify\n3. Remove\n---> ".encode('utf-8'))
        action = get_selection(conn, ["1", "2", "3"])

        if action == "1":
            AddArtistNomination("Add Artist Nomination").exec(conn)
        elif action == "2":
            ModifyArtistNomination("Modify Artist Nomination").exec(conn)
        elif action == "3":
            RemoveArtistNomination("Remove Artist Nomination").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
