import sqlite3
from sqlite3 import Error
from dbhelper import DBHelper


db = DBHelper()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM lastRequest")
   # cur.execute("SELECT * FROM items")
    rows = cur.fetchall()

    for row in rows:
        print(row)

def selectRequest(conn):
    cur = conn.cursor()
    #cur.execute("SELECT request FROM lastRequest WHERE chatID = ? ", (chatID,) )
    cur.execute("SELECT * FROM requests ")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    #return rows[0][0]

def selectErrors(conn):
    cur = conn.cursor()
    #cur.execute("SELECT request FROM lastRequest WHERE chatID = ? ", (chatID,) )
    cur.execute("SELECT * FROM errors ")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():
    #db.drop()
    db.setup()
    db.updateLastRequest(1,"russia")
    select_all_tasks(create_connection("/Users/frozmannik/PycharmProjects/WikiBot/wikiSearch.sqlite"))

    #db.insertRequest(666, "Russia")
    selectRequest(create_connection("/Users/frozmannik/PycharmProjects/WikiBot/wikiSearch.sqlite"))

    try:
        "qwe"/2
    except Exception as e:
        print("ERROR")
        db.insertError(666,'test',e)

    selectErrors(create_connection("/Users/frozmannik/PycharmProjects/WikiBot/wikiSearch.sqlite"))



if __name__ == '__main__':
    main()