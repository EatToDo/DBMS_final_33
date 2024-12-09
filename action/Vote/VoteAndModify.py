from ..Action import Action
from DB_utils import get_max_ceremony_id, list_nominated, vote, list_vote_today, list_validvote_today
import time

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
        conn.send("\n========================================================\n".encode('utf-8'))
        conn.send("Welcome to the voting system!\n".encode('utf-8'))

        ceremony_id = get_max_ceremony_id()
        if not ceremony_id:
            conn.send("No ceremony found.\n".encode('utf-8'))
            return

        formatted_ceremony = self.format_ceremony_id(ceremony_id)
        conn.send(f"This page is the voting system for the {formatted_ceremony} ceremony!\n\n".encode('utf-8'))

        conn.sendall("Notices:\n- Each user can only vote once per day.\n- Please confirm your choice. You can delete or modify your vote before 23:59 today.\n".encode('utf-8'))

        table, options = list_nominated(ceremony_id)

        table_vote, result = list_vote_today(userid)
        table_validvote, result = list_validvote_today(userid)
        print(result)
        if not result:
            while True:
                conn.send("\nPlease enter the number corresponding to your selection:\n".encode('utf-8'))
                for i, option in enumerate(options, start=1):
                    conn.send(f"{i}. {option}\n".encode('utf-8'))
                conn.send(f"{len(options) + 1}. Go back to the previous menu\n".encode('utf-8'))

                selection = self.read_input(conn, "your selection")

                try:
                    selection = int(selection)
                    if 1 <= selection <= len(options):
                        selected_option = options[selection - 1]
                        vote(userid, selected_option, ceremony_id)
                        conn.send(f"\nYou selected: {selected_option}\n".encode('utf-8'))
                        conn.send(f"\nCongrats!!! Your selection: {selected_option} has been recorded successfully!\n".encode('utf-8'))
                        break
                    elif selection == len(options) + 1:
                        conn.send("\nReturning to the previous menu...\n".encode('utf-8'))
                        return
                    else:
                        conn.send(f"\nInvalid selection. Please select a number between 1 and {len(options) + 1}.\n".encode('utf-8'))
                except ValueError:
                    conn.send("\nInvalid input. Please enter a number.\n".encode('utf-8'))

        else:
            conn.send(f"\nBelow are your voting record today.\n".encode('utf-8'))
            table_validvote, result = list_validvote_today(userid)
            self.send_table(conn, table_validvote)
            conn.send("\n".encode('utf-8'))
            reply = self.read_input(conn, "'Yes' to modify your vote today, the other word to cancel")
            if reply == 'Yes':
                while True:
                    conn.send("\nPlease enter the number corresponding to your selection:\n".encode('utf-8'))
                    for i, option in enumerate(options, start=1):
                        conn.send(f"{i}. {option}\n".encode('utf-8'))
                    conn.send(f"{len(options) + 1}. Go back to the previous menu\n".encode('utf-8'))
                    conn.send("\n".encode('utf-8'))
                    selection = self.read_input(conn, "your selection")

                    try:
                        selection = int(selection)
                        if 1 <= selection <= len(options):
                            selected_option = options[selection - 1]
                            vote(userid, selected_option, ceremony_id)
                            conn.send(f"\nYou selected: {selected_option}".encode('utf-8'))
                            conn.send(f"\nCongrats!!! Your selection: {selected_option} has been recorded successfully!\n".encode('utf-8'))
                            break
                        elif selection == len(options) + 1:
                            conn.send("\n\nReturning to the previous menu...\n".encode('utf-8'))
                            return
                        else:
                            conn.send(f"\n\nInvalid selection. Please select a number between 1 and {len(options) + 1}.\n".encode('utf-8'))
                    except ValueError:
                        conn.send("\n\nInvalid input. Please enter a number.\n".encode('utf-8'))




