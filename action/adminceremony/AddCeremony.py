from DB_utils import add_ceremony, ceremony_id_exist
from ..Action import Action

class AddCeremony(Action):
    def exec(self, conn):
        """
        Add a new ceremony.
        """
        ceremony_id = self.read_input(conn, "ceremony ID (unique)")
        year = self.read_input(conn, "year (e.g., 1990)")
        host = self.read_input(conn, "host (type null if unknown)")
        jury_chairperson = self.read_input(conn, "jury chairperson (type null if unknown)")
        location = self.read_input(conn, "location(type null if unknown)")
        if ceremony_id_exist(ceremony_id):
            conn.send(f"\nCeremony ID {ceremony_id} already exists! Please choose a unique ID.\n".encode('utf-8'))
            return

        try:
            add_ceremony(ceremony_id, year, host, jury_chairperson, location)
            conn.send(f"\nCeremony with ID {ceremony_id} added successfully!\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to add ceremony: {e}\n".encode('utf-8'))
