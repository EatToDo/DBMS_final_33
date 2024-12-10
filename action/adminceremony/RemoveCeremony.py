from DB_utils import remove_ceremony, ceremony_exist
from ..Action import Action

class RemoveCeremony(Action):
    def exec(self, conn):
        """
        Remove a ceremony.
        """
        ceremony_id = self.read_input(conn, "ceremony ID")

        if not ceremony_exist(ceremony_id):
            conn.send(f"\nCeremony ID {ceremony_id} does not exist!\n".encode('utf-8'))
            return

        try:
            remove_ceremony(ceremony_id)
            conn.send(f"\nCeremony ID {ceremony_id} removed successfully.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to remove ceremony: {e}\n".encode('utf-8'))
