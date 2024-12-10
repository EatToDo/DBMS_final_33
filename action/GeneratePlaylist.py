from action.Action import Action
from DB_utils import fetch_random_songs

class GeneratePlaylist(Action):
    def exec(self, conn, user):
        try:
           
            song_count = self.read_input(conn, "Enter the number of songs for the playlist")
            song_count = int(song_count)

            
            playlist = fetch_random_songs(song_count)

            
            playlist_output = "\nGenerated Playlist:\n"
            for i, song in enumerate(playlist, start=1):
                playlist_output += f"{i}. {song[1]} - {song[2]} ({song[3]})\n"

            conn.send(playlist_output.encode('utf-8'))
        except ValueError:
            conn.send("\nInvalid input. Please enter a valid number.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"\nFailed to generate playlist: {e}\n".encode('utf-8'))
