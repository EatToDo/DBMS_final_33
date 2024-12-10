from DB_utils import update_ceremony, ceremony_exist
from ..Action import Action
from utils import list_option, get_selection

class ModifyCeremony(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["year", "host", "jury_chairperson", "location"]

    def exec(self, conn):
        """
        Modify an existing ceremony.
        """
        ceremony_id = self.read_input(conn, "ceremony ID")

        if not ceremony_exist(ceremony_id):
            conn.send(f"\nCeremony ID {ceremony_id} does not exist!\n".encode('utf-8'))
            return

        msg = '[INPUT] Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        select_item = get_selection(conn, self.options)
        new_value = self.read_input(conn, f"new value for {select_item}")

        try:
            update_ceremony(ceremony_id, select_item, new_value)
            conn.send(f"\nCeremony ID {ceremony_id} modified successfully.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to modify ceremony: {e}\n".encode('utf-8'))
