from ..Action import Action
from utils import list_option, get_selection
from .AddSong import AddSong
from .ModifySong import ModifySong
from .RemoveSong import RemoveSong



class ManageSong(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [
            AddSong("Add Song"),
            ModifySong("Modify Song"),
            RemoveSong("Remove Song"),
       
           

        ]

    def exec(self, conn, user):
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        action = get_selection(conn, self.options)
        action.exec(conn)
