from ..Action import Action
from DB_utils import update_album, album_exist
from utils import list_option, get_selection

class ModifyAlbum(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = ["title", "release_year", "artist_id"]

    def exec(self, conn):
        album_id = self.read_input(conn, "album ID")

        if not album_exist(album_id):
            conn.send(f'\nAlbum does not exist!\n'.encode('utf-8'))
            return

        msg = '[INPUT]Which field do you want to modify?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))
        select_item = get_selection(conn, self.options)
        new_value = self.read_input(conn, f'new value for {select_item}')

        try:
            update_album(album_id, select_item, new_value)
            conn.send(f'\nAlbum modified successfully!\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\nFailed to modify album: {e}\n'.encode('utf-8'))
