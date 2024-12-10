from ..Action import Action
from utils import list_option, get_selection
from .AddArtist import AddArtist
from .ModifyArtist import ModifyArtist
from .RemoveArtist import RemoveArtist

class ManageArtist(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [
            AddArtist("Add Artist"),
            ModifyArtist("Modify Artist"),
            RemoveArtist("Remove Artist")
        ]

    def exec(self, conn, user):
        # 顯示操作選單
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        # 根據選擇執行對應的功能
        action = get_selection(conn, self.options)
        action.exec(conn)
