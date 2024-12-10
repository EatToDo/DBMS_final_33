from ..Action import Action
from utils import list_option, get_selection
from .AddPerformance import AddPerformance
from .ModifyPerformance import ModifyPerformance
from .RemovePerformance import RemovePerformance

class ManagePerformance(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.options = [
            AddPerformance("Add Performance"),
            ModifyPerformance("Modify Performance"),
            RemovePerformance("Remove Performance")
        ]

    def exec(self, conn, user):
        # 顯示操作選單
        msg = '[INPUT]What do you want to do?\n' + list_option(self.options) + '---> '
        conn.send(msg.encode('utf-8'))

        # 根據選擇執行對應的功能
        action = get_selection(conn, self.options)
        action.exec(conn)
