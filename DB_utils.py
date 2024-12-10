import sys
import psycopg2
from tabulate import tabulate
from threading import RLock

DB_NAME = "final"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

cur = None
db = None
create_event_lock = RLock()

lock_pool = {}

def get_lock(comment_id):
    if comment_id not in lock_pool:
        lock_pool[comment_id] = RLock()
    return lock_pool[comment_id]

def db_connect():
    exit_code = 0
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='zaq123789',
                              host=DB_HOST, port=DB_PORT)
        print("Successfully connect to DBMS.")
        global cur
        cur = db.cursor()
        return db

    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    # finally:
    #     if db is not None:
    #         db.close()
    sys.exit(exit_code)

def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")

def print_table_with_no(cur, visible_columns=None):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    table = [(idx, *row) for idx, row in enumerate(rows, start=1)]

    if visible_columns is None:
        visible_columns = columns

    visible_indexes = [columns.index(col) + 1 for col in visible_columns]

    filtered_table = [
        (row[0], *(row[i] for i in visible_indexes)) for row in table
    ]

    headers = ["No."] + visible_columns
    formatted_table = tabulate(filtered_table, headers=headers, tablefmt="github")

    return table, formatted_table

# ============================= System function =============================
def db_register_user(username, pwd, gender, bdate):
    try:
        cmd =   """
                insert into "users" (username, password, gender, bdate, role) values (%s, %s, %s, %s, 'User')
                RETURNING user_id;
                """
        cur.execute(cmd, [username, pwd, gender, bdate])
        userid = cur.fetchone()[0]
        if userid is None:
                raise ValueError("Failed to retrieve user ID after insertion.")

        db.commit()
        return userid
    except Exception as e:
            print(f"Error during user registration: {e}")
            db.rollback()
            raise e

def fetch_user(userid):
    cmd =   """
            select *
            from "users" u
            where u.User_id = %s;
            """
    cur.execute(cmd, [userid])

    rows = cur.fetchall()
    if not rows:
        return None, None, None, None, None, None
    else:
        isUser = False
        isAdmin = False
        for row in rows:
            userid, username, pwd, gender, bdate, role = row

            if role == 'User':
                isUser = True
            elif role == 'Admin':
                isAdmin = True

    return username, pwd, gender, bdate, isUser, isAdmin

def username_exist(username):
    try:
        cmd = """
            SELECT COUNT(*) FROM "users"
            WHERE Username = %s;
            """
        cur.execute(cmd, [username])
        count = cur.fetchone()[0]
        return count > 0

    except Exception as e:
        print(f"Error during username existence check: {e}")
        db.rollback()
        return False

def userid_exist(userid):
    cmd =   """
            select count(*)
            from "users"
            where user_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0


# ============================= function for User =============================
def update_user_info(userid, item, new_value):
    try:
        cmd =  f"""
                update "users"
                set {item} = %s
                where user_id = %s;
                """
        print(f'Update User Info | {userid}: {item}->{new_value}')
        cur.execute(cmd, [new_value, userid])
        print(f'After update')
        db.commit()
        return
    except Exception as e:
        db.rollback()
        print(f"Error updating user info: {e}")
        raise

def get_max_ceremony_id():
    try:
        cmd = """
            SELECT MAX(ceremony_id) AS max_ceremony_id
            FROM "artists_nomination";
        """
        cur.execute(cmd)

        result = cur.fetchone()

        return result[0] if result and result[0] is not None else None

    except Exception as e:
        print(f"Error: An exception occurred while executing the SQL command: {e}")
        return None

def list_nominated(ceremony_id):
    if not ceremony_id:
        raise ValueError("Ceremony ID cannot be None or empty.")

    cmd = """
        SELECT name
        FROM "artists_nomination" AS an
        JOIN "artists" AS a ON an.artist_id = a.artist_id
        WHERE ceremony_id = %s;
        """

    cur.execute(cmd, [ceremony_id])
    rows = cur.fetchall()

    numbered_rows = [(idx + 1, row[0]) for idx, row in enumerate(rows)]
    formatted_table = tabulate(numbered_rows, headers=["No.", "Name"], tablefmt="github")
    options = [row[0] for row in rows]

    return formatted_table, options


def vote(userid, artist, cid):
    try:
        cmd_get_aid = """
            SELECT artist_id
            FROM "artists"
            WHERE name = %s;
        """
        cur.execute(cmd_get_aid, [artist])
        result = cur.fetchone()
        aid = result[0]

        if not result:
            raise ValueError(f"Artist '{artist}' not found in the database.")

        cmd_check_vote_today = """
            SELECT user_id, vote_timestamp, status
            FROM "popular_singer_votes"
            WHERE user_id = %s AND ceremony_id = %s AND DATE(vote_timestamp) = CURRENT_DATE;
        """
        cur.execute(cmd_check_vote_today, [userid, cid])
        existing_vote = cur.fetchone()

        if existing_vote:
            cmd_update_vote = """
                UPDATE "popular_singer_votes"
                SET status = '已刪除'
                WHERE user_id = %s AND ceremony_id = %s AND DATE(vote_timestamp) = CURRENT_DATE;
            """
            cur.execute(cmd_update_vote, [userid, cid])

            cmd_insert_vote = """
                INSERT INTO popular_singer_votes(user_id, artist_id, ceremony_id, vote_timestamp, status)
                VALUES (%s, %s, %s, NOW(), '有效');
            """
            cur.execute(cmd_insert_vote, [userid, aid, cid])

            db.commit()
            print("Vote recorded successfully.")


        else:
            cmd_insert_vote = """
                INSERT INTO popular_singer_votes(user_id, artist_id, ceremony_id, vote_timestamp, status)
                VALUES (%s, %s, %s, NOW(), '有效');
            """
            cur.execute(cmd_insert_vote, [userid, aid, cid])

            db.commit()
            print("Vote recorded successfully.")


    except ValueError as ve:
        print(f"Validation Error: {ve}")
        db.rollback()
    except Exception as e:
        print(f"Error in record_vote: {e}")
        db.rollback()
        raise

def list_vote_today(user_id):
    cmd = """
        SELECT a.name AS the_artists_you_chose_today, vote_timestamp, status
        FROM "popular_singer_votes" AS v
        JOIN "artists" AS a ON v.artist_id = a.artist_id
        WHERE v.user_id = %s AND DATE(v.vote_timestamp) = CURRENT_DATE;
        """

    cur.execute(cmd, [user_id])
    result = cur.fetchone()
    return print_table(cur), result

def list_validvote_today(user_id):
    cmd = """
        SELECT a.name AS the_artists_you_chose_today, vote_timestamp, status
        FROM "popular_singer_votes" AS v
        JOIN "artists" AS a ON v.artist_id = a.artist_id
        WHERE v.user_id = %s AND DATE(v.vote_timestamp) = CURRENT_DATE AND status = '有效';
        """

    cur.execute(cmd, [user_id])
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return tabulate(rows, headers=columns, tablefmt="github"), rows

def delete_vote(user_id, ceremony_id):
    cmd = """
        UPDATE "popular_singer_votes"
        SET status = '已刪除'
        WHERE user_id = %s AND ceremony_id = %s AND DATE(vote_timestamp) = CURRENT_DATE;
        """
    cur.execute(cmd, [user_id, ceremony_id])
    db.commit()

def list_vote(user_id):
    cmd = """
        SELECT a.name AS the_artists_you_chose, ceremony_id, DATE(vote_timestamp) AS vote_date, status
        FROM "popular_singer_votes" AS v
        JOIN "artists" AS a ON v.artist_id = a.artist_id
        WHERE v.user_id = %s AND status = '有效'
        ORDER BY vote_timestamp DESC;
        """

    cur.execute(cmd, [user_id])
    return print_table_with_no(cur)

def list_ceremony_vote(ceremony_id):
    cmd = """
        SELECT a.name, COUNT(*) AS total_votes
        FROM popular_singer_votes AS v
        JOIN artists AS a ON v.artist_id = a.artist_id
        WHERE ceremony_id = %s AND status = '有效'
        GROUP BY a.name
        ORDER BY total_votes DESC;
    """

    cur.execute(cmd, [ceremony_id])
    return print_table(cur)

def fetch_all_ceremony():
    cmd = """
        SELECT DISTINCT ceremony_id FROM performance;
    """

    cur.execute(cmd)
    results = cur.fetchall()
    return [row[0] for row in results]

def fetch_performance_ceremony(ceremony_id):
    cmd = """
        SELECT a.name AS artist_name, p.performance_name
        FROM performance AS p
        JOIN performance_artists AS pa ON p.performance_id = pa.performance_id
        JOIN artists AS a ON pa.artist_id = a.artist_id
        WHERE p.ceremony_id = %s;
    """

    cur.execute(cmd, [ceremony_id])
    results = cur.fetchall()
    return [(row[0], row[1]) for row in results]

def get_performance_id(ceremony_id, performance_name):
    cmd = """
        SELECT performance_id
        FROM performance
        WHERE ceremony_id = %s AND performance_name = %s;
    """
    cur.execute(cmd, [ceremony_id, performance_name])
    results = cur.fetchone()
    print(ceremony_id)
    print(performance_name)
    return results[0]

def comment(performance_id, userid, comment_text):
    cmd = """
        INSERT INTO performance_comments(performance_id, user_id, comment_text, comment_timestamp, status)
        VALUES (%s, %s, %s, NOW(), '有效');
    """

    cur.execute(cmd, [performance_id, userid, comment_text])
    db.commit()
    print("Comment recorded successfully.")

def list_comment(performance_id):
    cmd ="""
        SELECT u.username, pc.comment_text
        FROM performance_comments AS pc
        JOIN users AS u ON pc.user_id = u.user_id
        WHERE pc.performance_id = %s;
    """

    cur.execute(cmd, [performance_id])
    print(cmd)
    return print_table(cur)

def list_your_comment(user_id):
    cmd = """
        SELECT pc.comment_id, p.performance_name, pc.comment_text
        FROM performance_comments AS pc
        JOIN performance AS p ON pc.performance_id = p.performance_id
        WHERE pc.user_id = %s AND status = '有效';
    """

    cur.execute(cmd, [user_id])
    return print_table_with_no(cur, visible_columns=["performance_name", "comment_text"])

def update_comment(comment_id, user_id, comment_text):
    lock = get_lock(comment_id)
    with lock:
        try:
            cmd_check = """
                SELECT status, performance_id
                FROM performance_comments
                WHERE comment_id = %s
                FOR UPDATE;
            """
            cur.execute(cmd_check, [comment_id])
            result = cur.fetchone()

            if not result:
                raise ValueError("Comment does not exist.")

            status, performance_id = result

            if status == '已刪除':
                raise ValueError("Cannot update a deleted comment.")

            cmd_update = """
                UPDATE performance_comments
                SET status = '已刪除'
                WHERE comment_id = %s;
            """
            cur.execute(cmd_update, [comment_id])

            cmd_insert = """
                INSERT INTO performance_comments(performance_id, user_id, comment_text, comment_timestamp, status)
                VALUES (%s, %s, %s, NOW(), '有效');
            """
            cur.execute(cmd_insert, [performance_id, user_id, comment_text])
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error occurred during comment update: {e}")
            raise

def delete_comment(comment_id):
    lock = get_lock(comment_id)
    lock.aquire
    with lock:
        try:
            cmd_check = """
                SELECT status
                FROM performance_comments
                WHERE comment_id = %s
                FOR UPDATE;
            """
            cur.execute(cmd_check, [comment_id])
            result = cur.fetchone()

            if not result:
                raise ValueError("Comment does not exist.")

            status = result[0]

            if status == '已刪除':
                print("Comment is already deleted.")
                return

            cmd_delete = """
                UPDATE performance_comments
                SET status = '已刪除'
                WHERE comment_id = %s;
            """
            cur.execute(cmd_delete, [comment_id])
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error occurred while deleting comment: {e}")
            raise

def search(category, type, name, award, ceremony):
    category_1 = category[:-1]
    if category == 'artists':
        query = f"""
            SELECT name, ceremony_id AS ceremony, nomination_name, a.gender AS {category_1}_gender, a.bdate AS {category_1}_birthday
            FROM {category}_nomination AS an
            JOIN {category} AS a ON an.{category_1}_id = a.{category_1}_id\n
        """
        if type == 'awards':
            query += "JOIN artists_awards AS aa ON an.nomination_id = aa.nomination_id\n"
        query += "WHERE "

        count = 0
        if name != "None":
            count += 1
            query += f"name LIKE '%{name}%'"
        if award != "None":
            if count != 0:
                query += " AND "
            count += 1
            query += f"nomination_name LIKE '%{award}%'"
        if ceremony != "None":
            if count != 0:
                query += " AND "
            count += 1
            query += f"ceremony_id = {ceremony}"

    else:
        if category == 'albums':
            query = f"""
                SELECT s.title AS album_name, sn.ceremony_id AS ceremony, sn.nomination_name, s.release_year, ar.name AS artist_name
                FROM albums_nomination AS sn
                JOIN albums AS s ON sn.album_id = s.album_id
                JOIN artists AS ar ON s.artist_id = ar.artist_id\n
            """
            if type == 'awards':
                query += "JOIN albums_awards AS aa ON aa.nomination_id = sn.nomination_id\n"

        else:
            query = f"""
                SELECT s.title AS song_name, sn.ceremony_id AS ceremony, sn.nomination_name, s.release_year, a.title AS album_name
                FROM songs_nomination AS sn
                JOIN songs AS s ON sn.song_id = s.song_id
                JOIN albums AS a ON s.album_id = a.album_id\n
            """
            if type == 'awards':
                query += "JOIN songs_awards AS aa ON aa.nomination_id = sn.nomination_id\n"


        query += "WHERE "
        count = 0

        if name != "None":
            count += 1
            query += f"s.title LIKE '%{name}%'"
        if award != "None":
            if count != 0:
                query += " AND "
            count += 1
            query += f"nomination_name LIKE '%{award}%'"
        if ceremony != "None":
            if count != 0:
                query += " AND "
            count += 1
            query += f"ceremony_id = {ceremony}"

    cur.execute(query)
    return print_table(cur)

# def fetch_performance_comments(performance_id):
#     """
#     Fetch comments for a specific performance.
#     """
#     cmd = """
#     SELECT comment_id, comment_text, user_id
#     FROM performance_comments
#     WHERE performance_id = %s;
#     """
#     try:
#         cur.execute(cmd, [performance_id])
#         return print_table(cur)
#     except Exception as e:
#         raise Exception(f"Failed to fetch comments for performance ID {performance_id}: {e}")

def append_song(title, release_year, album_id):
    cmd = """
    INSERT INTO songs (title, release_year, album_id)
    VALUES (%s, %s, %s) RETURNING song_id;
    """
    try:
        cur.execute(cmd, [title, release_year, album_id])
        db.commit()
        return cur.fetchone()[0]
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add song: {e}")



def song_exist(song_id):
    cmd = "SELECT COUNT(*) FROM songs WHERE song_id = %s;"
    cur.execute(cmd, [song_id])
    return cur.fetchone()[0] > 0

def update_song(song_id, field, value):
    # 確保欄位名稱合法
    valid_fields = ["title", "release_year", "album_id"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    # 更新指定欄位的值
    cmd = f"UPDATE songs SET {field} = %s WHERE song_id = %s;"
    try:
        cur.execute(cmd, [value, song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update song: {e}")




def remove_song(song_id):
    try:
        # Step 1: 查找與歌曲相關的提名 ID
        cmd_get_nomination_ids = """
        SELECT nomination_id FROM songs_nomination WHERE song_id = %s;
        """
        cur.execute(cmd_get_nomination_ids, [song_id])
        nomination_ids = [row[0] for row in cur.fetchall()]

        # Step 2: 刪除與提名 ID 相關的得獎記錄
        if nomination_ids:
            cmd_delete_awards = """
            DELETE FROM songs_awards WHERE nomination_id = ANY(%s);
            """
            cur.execute(cmd_delete_awards, [nomination_ids])

        # Step 3: 刪除歌曲的提名記錄
        cmd_delete_nominations = """
        DELETE FROM songs_nomination WHERE song_id = %s;
        """
        cur.execute(cmd_delete_nominations, [song_id])

        # Step 4: 刪除歌曲合作關係
        cmd_delete_collaborations = """
        DELETE FROM song_collaborations WHERE song_id = %s;
        """
        cur.execute(cmd_delete_collaborations, [song_id])

        # Step 5: 刪除歌曲記錄
        cmd_delete_song = """
        DELETE FROM songs WHERE song_id = %s;
        """
        cur.execute(cmd_delete_song, [song_id])

        # 提交更改
        db.commit()
        print(f"Song {song_id} and related records removed successfully.")

    except Exception as e:
        db.rollback()  # 回滾交易
        raise Exception(f"Failed to remove song and related records: {e}")

def append_album(title, release_year, artist_id):
    cmd = """
    INSERT INTO albums (title, release_year, artist_id)
    VALUES (%s, %s, %s) RETURNING album_id;
    """
    try:
        cur.execute(cmd, [title, release_year, artist_id])
        db.commit()
        return cur.fetchone()[0]
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add album: {e}")
def update_album(album_id, field, value):
    valid_fields = ["title", "release_year", "artist_id"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE albums SET {field} = %s WHERE album_id = %s;"
    try:
        cur.execute(cmd, [value, album_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update album: {e}")

def remove_album(album_id):
    """
    Remove an album by ID from the database, including handling related songs.
    :param album_id: The ID of the album to be removed.
    """
    try:
        # 確認專輯是否存在
        if not album_exist(album_id):
            raise Exception(f"Album with ID {album_id} does not exist.")

        # Step 1: 查找與專輯相關的歌曲
        cmd_get_songs = "SELECT song_id FROM songs WHERE album_id = %s;"
        cur.execute(cmd_get_songs, [album_id])
        song_ids = [row[0] for row in cur.fetchall()]

        # Step 2: 刪除相關的歌曲及其數據
        for song_id in song_ids:
            remove_song(song_id)  # 調用已實作的 remove_song 函數

        # Step 3: 刪除專輯
        cmd_delete_album = "DELETE FROM albums WHERE album_id = %s;"
        cur.execute(cmd_delete_album, [album_id])

        # 提交更改
        db.commit()
        print(f"Album {album_id} and related songs removed successfully.")
    except Exception as e:
        db.rollback()  # 回滾變更
        print(f"Failed to remove album {album_id}: {e}")
        raise e


def album_exist(album_id):

    cmd_check_album = "SELECT 1 FROM albums WHERE album_id = %s;"
    try:
        cur.execute(cmd_check_album, [album_id])
        return cur.fetchone() is not None
    except Exception as e:
        print(f"Error checking if album exists: {e}")
        raise e



def append_artist(name, gender, bdate):
    cmd = """
    INSERT INTO artists (name, gender, bdate)
    VALUES (%s, %s, %s) RETURNING artist_id;
    """
    try:
        cur.execute(cmd, [name, gender, bdate])
        db.commit()
        return cur.fetchone()[0]
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add artist: {e}")
def update_artist(artist_id, field, value):
    valid_fields = ["name", "gender", "bdate"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE artists SET {field} = %s WHERE artist_id = %s;"
    try:
        cur.execute(cmd, [value, artist_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update artist: {e}")
def remove_artist(artist_id):
    """
    Remove an artist by ID from the database, including related albums, songs, performances, and votes.
    :param artist_id: The ID of the artist to be removed.
    """
    try:
        # Step 1: 刪除歌手的專輯及歌曲
        cmd_get_albums = "SELECT album_id FROM albums WHERE artist_id = %s;"
        cur.execute(cmd_get_albums, [artist_id])
        album_ids = [row[0] for row in cur.fetchall()]

        for album_id in album_ids:
            remove_album(album_id)  # 調用之前實現的 remove_album 函數

        # Step 2: 刪除合作歌曲
        cmd_delete_collaborations = """
        DELETE FROM song_collaborations WHERE collaborator_id = %s;
        """
        cur.execute(cmd_delete_collaborations, [artist_id])

        # Step 3: 刪除歌手的表演
        cmd_get_performances = """
        SELECT performance_id FROM performance_artists WHERE artist_id = %s;
        """
        cur.execute(cmd_get_performances, [artist_id])
        performance_ids = [row[0] for row in cur.fetchall()]

        for performance_id in performance_ids:
            # 刪除 performance_artists 中的記錄
            cmd_delete_performance_artist = """
            DELETE FROM performance_artists WHERE performance_id = %s AND artist_id = %s;
            """
            cur.execute(cmd_delete_performance_artist, [performance_id, artist_id])
        # Step 2: 刪除合作歌曲
            cmd_delete_collaborations = """
        DELETE FROM song_collaborations WHERE collaborator_id = %s OR song_id IN (
            SELECT song_id FROM songs WHERE album_id IN (
                SELECT album_id FROM albums WHERE artist_id = %s
            )
        );
        """
            # 檢查該表演是否僅剩該歌手
            cmd_check_remaining_artists = """
            SELECT COUNT(*) FROM performance_artists WHERE performance_id = %s;
            """
            cur.execute(cmd_check_remaining_artists, [performance_id])
            remaining_artists = cur.fetchone()[0]

            if remaining_artists == 0:
                # 刪除表演和相關評論
                cmd_delete_performance_comments = """
                DELETE FROM performance_comments WHERE performance_id = %s;
                """
                cur.execute(cmd_delete_performance_comments, [performance_id])

                cmd_delete_performance = "DELETE FROM performance WHERE performance_id = %s;"
                cur.execute(cmd_delete_performance, [performance_id])

        # Step 4: 刪除人氣投票
        cmd_delete_votes = """
        DELETE FROM popular_singer_votes WHERE artist_id = %s;
        """
        cur.execute(cmd_delete_votes, [artist_id])

        # Step 5: 刪除歌手記錄
        cmd_delete_artist = "DELETE FROM artists WHERE artist_id = %s;"
        cur.execute(cmd_delete_artist, [artist_id])

        # 提交更改
        db.commit()
        print(f"Artist {artist_id} and related records removed successfully.")
    except Exception as e:
        db.rollback()  # 回滾變更
        print(f"Failed to remove artist {artist_id}: {e}")
        raise e

def artist_exist(artist_id):
    """
    檢查歌手是否存在
    """
    cmd = "SELECT 1 FROM artists WHERE artist_id = %s;"
    try:
        cur.execute(cmd, [artist_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if artist exists: {e}")

def fetch_random_songs(song_count):
    try:
        cmd = """
        SELECT s.song_id, s.title, a.title AS album_title, ar.name AS artist_name
        FROM songs s
        JOIN albums a ON s.album_id = a.album_id
        JOIN artists ar ON a.artist_id = ar.artist_id;
        """
        cur.execute(cmd)
        songs = cur.fetchall()

        if len(songs) < song_count:
            raise ValueError(f"Not enough songs available. Total songs: {len(songs)}.")

        # 隨機選取
        import random
        selected_songs = random.sample(songs, song_count)

        return selected_songs
    except Exception as e:
        raise Exception(f"Failed to fetch random songs: {e}")
def remove_performance(performance_id):
    try:
        # 刪除相關評論
        cmd_delete_comments = """
        DELETE FROM performance_comments WHERE performance_id = %s;
        """
        cur.execute(cmd_delete_comments, [performance_id])

        # 刪除表演歌手
        cmd_delete_artists = """
        DELETE FROM performance_artists WHERE performance_id = %s;
        """
        cur.execute(cmd_delete_artists, [performance_id])

        # 刪除表演
        cmd_delete_performance = """
        DELETE FROM performance WHERE performance_id = %s;
        """
        cur.execute(cmd_delete_performance, [performance_id])

        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove performance {performance_id}: {e}")


def update_performance(performance_id, field, value):
    valid_fields = ["ceremony_id", "performance_name"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE performance SET {field} = %s WHERE performance_id = %s;"
    try:
        cur.execute(cmd, [value, performance_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update performance: {e}")

def add_performance(ceremony_id, performance_name):
    """
    Add a new performance to the database.
    :param ceremony_id: The ID of the ceremony associated with the performance.
    :param performance_name: The name of the performance.
    :return: The ID of the newly added performance.
    """
    cmd = """
    INSERT INTO performance (ceremony_id, performance_name)
    VALUES (%s, %s) RETURNING performance_id;
    """
    try:
        cur.execute(cmd, [ceremony_id, performance_name])
        db.commit()
        return cur.fetchone()[0]
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add performance: {e}")
def performance_exist(performance_id):
    """
    Check if a performance exists in the database.
    :param performance_id: The ID of the performance.
    :return: True if the performance exists, False otherwise.
    """
    cmd = "SELECT 1 FROM performance WHERE performance_id = %s;"
    try:
        cur.execute(cmd, [performance_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if performance exists: {e}")

def add_performance_artist(performance_id, artist_id):
    cmd = """
    INSERT INTO performance_artists (performance_id, artist_id)
    VALUES (%s, %s);
    """
    try:
        cur.execute(cmd, [performance_id, artist_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add artist {artist_id} to performance {performance_id}: {e}")
def remove_performance_artist(performance_id, artist_id):
    cmd = """
    DELETE FROM performance_artists WHERE performance_id = %s AND artist_id = %s;
    """
    try:
        cur.execute(cmd, [performance_id, artist_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove artist {artist_id} from performance {performance_id}: {e}")




def get_performance_artists(performance_id):
    cmd = """
    SELECT artist_id FROM performance_artists WHERE performance_id = %s;
    """
    try:
        cur.execute(cmd, [performance_id])
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        raise Exception(f"Failed to fetch artists for performance {performance_id}: {e}")
def add_song_nomination(song_id, award, ceremony_id):
    """
    Add a nomination for a song.
    :param song_id: ID of the nominated song
    :param award: The award name/category
    :param ceremony_id: The ID of the ceremony
    :return: The ID of the newly added nomination
    """
    cmd = """
    INSERT INTO songs_nomination (song_id, nomination_name, ceremony_id)
    VALUES (%s, %s, %s) RETURNING nomination_id;
    """
    try:
        cur.execute(cmd, [song_id, award, ceremony_id])
        nomination_id = cur.fetchone()[0]
        db.commit()
        print(f"Song nomination added successfully with ID: {nomination_id}")
        return nomination_id
    except Exception as e:
        db.rollback()
        print(f"Failed to add song nomination: {e}")
        raise e
def update_song_nomination(nomination_id, field, value):
    """
    Update a song nomination.
    :param nomination_id: The ID of the nomination to update
    :param field: The field to update (e.g., "nomination_name", "ceremony_id")
    :param value: The new value for the field
    """
    valid_fields = ["nomination_name", "ceremony_id"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE songs_nomination SET {field} = %s WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [value, nomination_id])
        db.commit()
        print(f"Song nomination ID {nomination_id} updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"Failed to update song nomination: {e}")
        raise e
def remove_song_nomination(nomination_id):
    """
    Remove a song nomination.
    :param nomination_id: The ID of the nomination to remove
    """
    cmd = "DELETE FROM songs_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        db.commit()
        print(f"Song nomination ID {nomination_id} removed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Failed to remove song nomination: {e}")
        raise e
def song_nomination_exist(nomination_id):
    """
    Check if a song nomination exists.
    :param nomination_id: The ID of the nomination to check
    :return: True if the nomination exists, False otherwise
    """
    cmd = "SELECT 1 FROM songs_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        return cur.fetchone() is not None
    except Exception as e:
        print(f"Failed to check if song nomination exists: {e}")
        raise e


def add_album_nomination(album_id, award, ceremony_id):
    """
    Add a nomination for an album.
    """
    cmd = """
    INSERT INTO albums_nomination (album_id, nomination_name, ceremony_id)
    VALUES (%s, %s, %s) RETURNING nomination_id;
    """
    try:
        cur.execute(cmd, [album_id, award, ceremony_id])
        nomination_id = cur.fetchone()[0]
        db.commit()
        print(f"Album nomination added successfully with ID: {nomination_id}")
        return nomination_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add album nomination: {e}")


def update_album_nomination(nomination_id, field, value):
    """
    Update an album nomination.
    """
    valid_fields = ["nomination_name", "ceremony_id"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE albums_nomination SET {field} = %s WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [value, nomination_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update album nomination: {e}")


def remove_album_nomination(nomination_id):
    """
    Remove an album nomination.
    """
    cmd = "DELETE FROM albums_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove album nomination: {e}")


def album_nomination_exist(nomination_id):
    """
    Check if an album nomination exists.
    """
    cmd = "SELECT 1 FROM albums_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if album nomination exists: {e}")


def add_artist_nomination(artist_id, award, ceremony_id):
    """
    Add a nomination for an artist.
    """
    cmd = """
    INSERT INTO artists_nomination (artist_id, nomination_name, ceremony_id)
    VALUES (%s, %s, %s) RETURNING nomination_id;
    """
    try:
        cur.execute(cmd, [artist_id, award, ceremony_id])
        nomination_id = cur.fetchone()[0]
        db.commit()
        print(f"Artist nomination added successfully with ID: {nomination_id}")
        return nomination_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add artist nomination: {e}")


def update_artist_nomination(nomination_id, field, value):
    """
    Update an artist nomination.
    """
    valid_fields = ["nomination_name", "ceremony_id"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE artists_nomination SET {field} = %s WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [value, nomination_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update artist nomination: {e}")


def remove_artist_nomination(nomination_id):
    """
    Remove an artist nomination.
    """
    cmd = "DELETE FROM artists_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove artist nomination: {e}")


def artist_nomination_exist(nomination_id):
    """
    Check if an artist nomination exists.
    """
    cmd = "SELECT 1 FROM artists_nomination WHERE nomination_id = %s;"
    try:
        cur.execute(cmd, [nomination_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if artist nomination exists: {e}")

def add_song_award(nomination_id):
    """
    Add a new award for a song.
    """
    cmd = """
    INSERT INTO songs_awards (nomination_id)
    VALUES (%s) RETURNING award_id;
    """
    try:
        cur.execute(cmd, [nomination_id])
        award_id = cur.fetchone()[0]
        db.commit()
        print(f"Song award added successfully with ID: {award_id}")
        return award_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add song award: {e}")
def song_award_exist(award_id):
    """
    Check if a song award exists.
    """
    cmd = "SELECT 1 FROM songs_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if song award exists: {e}")
def remove_song_award(award_id):
    """
    Remove an award for a song.
    """
    cmd = "DELETE FROM songs_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        db.commit()
        print(f"Song award with ID {award_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove song award: {e}")



def add_artist_award(nomination_id):
    """
    Add a new award for a song.
    """
    cmd = """
    INSERT INTO artists_awards (nomination_id)
    VALUES (%s) RETURNING award_id;
    """
    try:
        cur.execute(cmd, [nomination_id])
        award_id = cur.fetchone()[0]
        db.commit()
        print(f"Artist award added successfully with ID: {award_id}")
        return award_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add artist award: {e}")

def artist_award_exist(award_id):
    """
    Check if a song award exists.
    """
    cmd = "SELECT 1 FROM artists_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if artist award exists: {e}")
def remove_artist_award(award_id):
    """
    Remove an award for a song.
    """
    cmd = "DELETE FROM artists_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        db.commit()
        print(f"Artist award with ID {award_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove artist award: {e}")




def add_album_award(nomination_id):
    """
    Add a new award for a song.
    """
    cmd = """
    INSERT INTO albums_awards (nomination_id)
    VALUES (%s) RETURNING award_id;
    """
    try:
        cur.execute(cmd, [nomination_id])
        award_id = cur.fetchone()[0]
        db.commit()
        print(f"Album award added successfully with ID: {award_id}")
        return award_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add album award: {e}")

def album_award_exist(award_id):
    """
    Check if a song award exists.
    """
    cmd = "SELECT 1 FROM albums_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if album award exists: {e}")

def remove_album_award(award_id):
    """
    Remove an award for a song.
    """
    cmd = "DELETE FROM albums_awards WHERE award_id = %s;"
    try:
        cur.execute(cmd, [award_id])
        db.commit()
        print(f"Album award with ID {award_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove album award: {e}")

def add_ceremony(ceremony_id, year, host, jury_chairperson, location):
    """
    Add a new ceremony to the database.
    """
    cmd = """
    INSERT INTO ceremony (ceremony_id, year, host, jury_chairperson, location)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cur.execute(cmd, [ceremony_id, year, host or None, jury_chairperson or None, location])
        db.commit()
        print(f"Ceremony with ID {ceremony_id} added successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add ceremony: {e}")


def update_ceremony(ceremony_id, field, value):
    """
    Update a ceremony record in the database.
    """
    valid_fields = ["year", "host", "jury_chairperson", "location"]
    if field not in valid_fields:
        raise Exception(f"Invalid field name: {field}")

    cmd = f"UPDATE ceremony SET {field} = %s WHERE ceremony_id = %s;"
    try:
        cur.execute(cmd, [value or None, ceremony_id])
        db.commit()
        print(f"Ceremony ID {ceremony_id} updated successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update ceremony: {e}")

def remove_ceremony(ceremony_id):
    """
    Remove a ceremony from the database.
    """
    cmd = "DELETE FROM ceremony WHERE ceremony_id = %s;"
    try:
        cur.execute(cmd, [ceremony_id])
        db.commit()
        print(f"Ceremony ID {ceremony_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove ceremony: {e}")

def ceremony_id_exist(ceremony_id):
    cmd = "SELECT 1 FROM ceremony WHERE ceremony_id = %s;"
    try:
        cur.execute(cmd, [ceremony_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if ceremony ID exists: {e}")

def ceremony_exist(ceremony_id):
    """
    Check if a ceremony exists in the database.
    """
    cmd = "SELECT 1 FROM ceremony WHERE ceremony_id = %s;"
    try:
        cur.execute(cmd, [ceremony_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if ceremony exists: {e}")

def fetch_performance_comments(performance_id):
    """
    Fetch comments for a specific performance.
    """
    cmd = """
    SELECT comment_id, comment_text, user_id
    FROM performance_comments
    WHERE performance_id = %s;
    """
    try:
        cur.execute(cmd, [performance_id])
        return cur.fetchall()
    except Exception as e:
        raise Exception(f"Failed to fetch comments for performance ID {performance_id}: {e}")

def comment_exist(comment_id):
    """
    Check if a comment exists.
    """
    cmd = "SELECT 1 FROM performance_comments WHERE comment_id = %s;"
    try:
        cur.execute(cmd, [comment_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if comment exists: {e}")



def remove_comment(comment_id):
    """
    Remove a comment by ID.
    """
    cmd = "DELETE FROM performance_comments WHERE comment_id = %s;"
    try:
        cur.execute(cmd, [comment_id])
        db.commit()
        print(f"Comment ID {comment_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove comment: {e}")

def fetch_highest_vote_singer(ceremony_id):
    """
    Fetch the highest vote singer for a specific ceremony.
    """
    cmd = """
    SELECT
        v.artist_id,
        a.name,
        COUNT(v.vote_id) AS total_votes
    FROM popular_singer_votes v
    JOIN artists a ON v.artist_id = a.artist_id
    WHERE v.ceremony_id = %s AND v.status = '有效'
    GROUP BY v.artist_id, a.name
    ORDER BY total_votes DESC
    LIMIT 1;
    """
    try:
        cur.execute(cmd, [ceremony_id])
        return cur.fetchone()
    except Exception as e:
        raise Exception(f"Failed to fetch highest vote singer for Ceremony ID {ceremony_id}: {e}")

def fetch_votes_for_ceremony(ceremony_id):
    """
    Fetch all votes for a specific ceremony.
    """
    cmd = """
    SELECT
        v.vote_id,
        v.user_id,
        v.artist_id,
        a.name,
        v.vote_timestamp,
        v.status
    FROM popular_singer_votes v
    JOIN artists a ON v.artist_id = a.artist_id
    WHERE v.ceremony_id = %s;
    """
    try:
        cur.execute(cmd, [ceremony_id])
        return cur.fetchall()
    except Exception as e:
        raise Exception(f"Failed to fetch votes for Ceremony ID {ceremony_id}: {e}")
def vote_exist(vote_id):
    """
    Check if a vote exists.
    """
    cmd = "SELECT 1 FROM popular_singer_votes WHERE vote_id = %s;"
    try:
        cur.execute(cmd, [vote_id])
        return cur.fetchone() is not None
    except Exception as e:
        raise Exception(f"Failed to check if vote exists: {e}")


def remove_vote(vote_id):
    """
    Remove a vote by ID.
    """
    cmd = "DELETE FROM popular_singer_votes WHERE vote_id = %s;"
    try:
        cur.execute(cmd, [vote_id])
        db.commit()
        print(f"Vote ID {vote_id} removed successfully.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove vote: {e}")
def fetch_vote_results_for_ceremony(ceremony_id):
    """
    Fetch vote counts for each artist in a specific ceremony.
    """
    cmd = """
    SELECT
        v.artist_id,
        a.name,
        COUNT(v.vote_id) AS total_votes
    FROM popular_singer_votes v
    JOIN artists a ON v.artist_id = a.artist_id
    WHERE v.ceremony_id = %s AND v.status = '有效'
    GROUP BY v.artist_id, a.name
    ORDER BY total_votes DESC;
    """
    try:
        cur.execute(cmd, [ceremony_id])
        return cur.fetchall()
    except Exception as e:
        raise Exception(f"Failed to fetch vote results for Ceremony ID {ceremony_id}: {e}")
