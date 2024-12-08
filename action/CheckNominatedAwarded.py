from .Action import Action
from DB_utils import search
from utils import list_option, get_selection
class CheckNominatedAwarded(Action):
    def __init__(self, action_name):
        super().__init__(action_name)
        self.option = ['Artists', 'Songs', 'Albums']
        self.type = ['Nominated', 'Awarded', 'Both']

    def exec(self, conn, user):
        print("CheckNominatedAwarded")

        msg = '[INPUT]Which category do you want to search for?\n' + list_option(self.option) + '---> '
        conn.send(msg.encode('utf-8'))
        category = get_selection(conn, self.option)
        category_mapping = {
            'Artists': 'artists',
            'Songs': 'songs',
            'Albums': 'albums'
        }
        category = category_mapping.get(category, category)

        msg = '[INPUT]Which category do you want to search for?\n' + list_option(self.type) + '---> '
        conn.send(msg.encode('utf-8'))
        type = get_selection(conn, self.type)

        type_mapping = {
            'Nominated': 'nomination',
            'Awarded': 'awards',
            'Both': 'both'
        }
        type = type_mapping.get(type, type)

        if type == 'both':
            conn.send(" (enter None if don't want to search based on the item)\n".encode('utf-8'))
            name = self.read_input(conn, f"the {category} name you want to search")
            award = self.read_input(conn, f"the award name you want to search")
            ceremony = self.read_input(conn, f"the ceremony you want to search")

            conn.send("The following is the information about the nomination\n".encode('utf-8'))
            nominated_table = search(category, 'nomination', name, award, ceremony)
            self.send_table(conn, nominated_table)
            conn.send("The following is the information about the awards\n".encode('utf-8'))
            award_table = search(category, 'awards', name, award, ceremony)
            self.send_table(conn, award_table)
            return

        else:
            conn.send(" (enter None if don't want to search based on the item)\n".encode('utf-8'))
            name = self.read_input(conn, f"the {category} name you want to search")
            award = self.read_input(conn, f"the award name you want to search")
            ceremony = self.read_input(conn, f"the ceremony you want to search")
            conn.send(f"The following is the information about the {type}\n".encode('utf-8'))
            table = search(category, type, name, award, ceremony)
            self.send_table(conn, table)
            return

