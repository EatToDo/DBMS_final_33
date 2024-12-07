from .Action import Action
from DB_utils import get_max_ceremony_id, list_nominated, vote, list_vote_today

class VoteAndModify(Action):

    @staticmethod
    def format_ceremony_id(ceremony_id):
        if 11 <= ceremony_id % 100 <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(ceremony_id % 10, "th")
        return f"{ceremony_id}{suffix}"

    def exec(self, conn, user):
        print("VoteAndModify")
        userid = user.get_userid()
        conn.send("Welcome to the voting system!\n".encode('utf-8'))

        ceremony_id = get_max_ceremony_id()
        if not ceremony_id:
            conn.send("No ceremony found.\n".encode('utf-8'))
            return

        formatted_ceremony = self.format_ceremony_id(ceremony_id)
        conn.send(f"This page is the voting system for the {formatted_ceremony} ceremony!\n\n".encode('utf-8'))

        conn.sendall("Notices:\n- Each user can only vote once per day.\n- Please confirm your choice. You can delete or modify your vote before 23:59 today.\n\n".encode('utf-8'))

        # conn.send("Below are the options you can vote for:\n".encode('utf-8'))
        table, options = list_nominated(ceremony_id)
        # conn.send(f"{table}\n".encode('utf-8'))

        conn.send(f"\nBelow are your voting record today.".encode('utf-8'))
        table_vote = list_vote_today(userid)
        self.send_table(conn, table_vote)

        # while True:
        #     conn.send("Please enter the number corresponding to your selection:\n".encode('utf-8'))
        #     selection = self.read_input(conn, "selection")

        #     try:
        #         selection = int(selection)
        #         if 1 <= selection <= len(options):
        #             selected_option = options[selection - 1]
        #             vote(userid, selected_option, ceremony_id)
        #             conn.send(f"You selected: {selected_option}\n".encode('utf-8'))
        #             break
        #         else:
        #             conn.send(f"Invalid selection. Please select a number between 1 and {len(options)}.\n".encode('utf-8'))
        #     except ValueError:
        #         conn.send("Invalid input. Please enter a number.\n".encode('utf-8'))

        while True:
            conn.send("Please enter the number corresponding to your selection:\n".encode('utf-8'))
            for i, option in enumerate(options, start=1):
                conn.send(f"{i}. {option}\n".encode('utf-8'))
            conn.send(f"{len(options) + 1}. Go back to the previous menu\n".encode('utf-8'))

            selection = self.read_input(conn, "selection")

            try:
                selection = int(selection)
                if 1 <= selection <= len(options):
                    selected_option = options[selection - 1]
                    vote(userid, selected_option, ceremony_id)
                    conn.send(f"You selected: {selected_option}\n".encode('utf-8'))
                    break
                elif selection == len(options) + 1:
                    conn.send("Returning to the previous menu...\n".encode('utf-8'))
                    return
                else:
                    conn.send(f"Invalid selection. Please select a number between 1 and {len(options) + 1}.\n".encode('utf-8'))
            except ValueError:
                conn.send("Invalid input. Please enter a number.\n".encode('utf-8'))




