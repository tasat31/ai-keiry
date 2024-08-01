import sqlite3

conn = sqlite3.connect("keiry.db", check_same_thread=False)

def db_read(sql):
    cursor = conn.cursor()
    res = cursor.execute(sql)
    return res


def db_write(sql):
    cursor = conn.cursor()

    try:
        cursor.execute(sql)

        conn.commit()
    except Exception as e:
        # Rollback the transaction on error
        conn.rollback()
        print(f"Error: {e}")
