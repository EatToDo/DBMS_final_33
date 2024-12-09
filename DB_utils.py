import sys
import psycopg2
from tabulate import tabulate
from threading import Lock

DB_NAME = "final"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

lock_pool = {}

def get_lock(comment_id):
    if comment_id not in lock_pool:
        lock_pool[comment_id] = Lock()
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

