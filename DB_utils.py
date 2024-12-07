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
    return print_table(cur)

def list_validvote_today(user_id):
    cmd = """
        SELECT a.name AS the_artists_you_chose_today, vote_timestamp, status
        FROM "popular_singer_votes" AS v
        JOIN "artists" AS a ON v.artist_id = a.artist_id
        WHERE v.user_id = %s AND DATE(v.vote_timestamp) = CURRENT_DATE AND status = '有效';
        """

    cur.execute(cmd, [user_id])
    return print_table(cur)

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
    return print_table(cur)

def list_your_comment(user_id):
    cmd = """
        SELECT pc.comment_id, p.performance_name, pc.comment_text
        FROM performance_comments AS pc
        JOIN performance AS p ON pc.performance_id = p.performance_id
        WHERE pc.user_id = %s AND status = '有效';
    """

    cur.execute(cmd, [user_id])
    return print_table_with_no(cur)

def update_comment(comment_id, user_id, comment_text):
    try:
        cmd_updata = """
            UPDATE performance_comments
            SET status = '已刪除'
            WHERE comment_id = %s
            RETURNING performance_id;
        """
        cur.execute(cmd_updata, [comment_id])
        performance_id = cur.fetchone()[0]

        cmd_insert = """
                INSERT INTO performance_comments(performance_id, user_id, comment_text, comment_timestamp, status)
                VALUES (%s, %s, %s, NOW(), '有效');
        """
        cur.execute(cmd_insert, [performance_id, user_id, comment_text])
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise

def delete_comment(comment_id):
    try:
        cmd = """
                UPDATE performance_comments
                SET status = '已刪除'
                WHERE comment_id = %s;
        """
        cur.execute(cmd, [comment_id])
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error occurred while deleting comment: {e}")
        raise