from .AddCeremony import AddCeremony
from .ModifyCeremony import ModifyCeremony
from .RemoveCeremony import RemoveCeremony
from ..Action import Action
from utils import list_option, get_selection

class ManageCeremony(Action):
    def exec(self, conn, user):
        """
        Manage ceremonies: Add, Modify, Remove.
        """
        conn.send("[INPUT] Choose an action:\n1. Add\n2. Modify\n3. Remove\n---> ".encode('utf-8'))
        action = get_selection(conn, ["1", "2", "3"])

        if action == "1":
            AddCeremony("Add Ceremony").exec(conn)
        elif action == "2":
            ModifyCeremony("Modify Ceremony").exec(conn)
        elif action == "3":
            RemoveCeremony("Remove Ceremony").exec(conn)
        else:
            conn.send("Invalid action. Returning to main menu.\n".encode('utf-8'))
