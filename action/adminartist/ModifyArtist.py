from ..Action import Action
from DB_utils import update_artist, artist_exist
from utils import list_option, get_selection

class ModifyArtist(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["name", "gender", "bdate"]

    def exec(self, conn):
        artist_id = self.read_input(conn, "artist ID")

        if not artist_exist(artist_id):
            conn.send(f'\nArtist does not exist!\n'.encode('utf-8'))
            return

        msg = '[INPUT]Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        select_item = get_selection(conn, self.options)
        new_value = self.read_input(conn, f'new value for {select_item}')

        try:
            update_artist(artist_id, select_item, new_value)
            conn.send(f'\nArtist modified successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to modify artist: {e}\n'.encode('utf-8'))
