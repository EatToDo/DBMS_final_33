from .AddAlbumNomination import AddAlbumNomination
from .ModifyAlbumNomination import ModifyAlbumNomination
from .RemoveAlbumNomination import RemoveAlbumNomination
from ..Action import Action
from utils import list_option, get_selection

class ManageAlbumNominations(Action):
    def exec(self, conn, user):
        """
        Manage album nominations: Add, Modify, Remove.
        """
        conn.send("[INPUT] Choose an action:\n1. Add\n2. Modify\n3. Remove\n---> ".encode('utf-8'))
        action = get_selection(conn, ["1", "2", "3"])

        if action == "1":
            AddAlbumNomination("Add Album Nomination").exec(conn)
        elif action == "2":
            ModifyAlbumNomination("Modify Album Nomination").exec(conn)
        elif action == "3":
            RemoveAlbumNomination("Remove Album Nomination").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
