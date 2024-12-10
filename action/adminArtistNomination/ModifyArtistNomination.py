from ..Action import Action
from DB_utils import update_artist_nomination, artist_nomination_exist
from utils import list_option, get_selection

class ModifyArtistNomination(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["nomination_name", "ceremony_id"]

    def exec(self, conn):
        """
        Modify an artist nomination in the database.
        """
        nomination_id = self.read_input(conn, "nomination ID")

        if not artist_nomination_exist(nomination_id):
            conn.send(f'\nNomination ID {nomination_id} does not exist!\n'.encode('utf-8'))
            return

        msg = '[INPUT] Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        select_item = get_selection(conn, self.options)
        new_value = self.read_input(conn, f'new value for {select_item}')

        try:
            update_artist_nomination(nomination_id, select_item, new_value)
            conn.send(f'\nNomination modified successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to modify nomination: {e}\n'.encode('utf-8'))
