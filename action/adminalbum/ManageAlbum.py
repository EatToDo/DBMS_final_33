from ..Action import Action
from utils import list_option, get_selection
from .AddAlbum import AddAlbum
from .ModifyAlbum import ModifyAlbum
from .RemoveAlbum import RemoveAlbum

class ManageAlbums(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [
            AddAlbum("Add Album"),
            ModifyAlbum("Modify Album"),
            RemoveAlbum("Remove Album"),
        ]

    def exec(self, conn, user):
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        action = get_selection(conn, self.options)
        action.exec(conn)
