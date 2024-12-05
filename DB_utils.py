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
