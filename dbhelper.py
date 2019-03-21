import sqlite3
import datetime


class DBHelper:

    def __init__(self, dbname="wikiSearch.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        try:
            createTable = """ CREATE TABLE IF NOT EXISTS lastRequest (
                                                    chatID integer PRIMARY KEY,
                                                    request text NOT NULL
                                                );"""
            self.conn.execute(createTable)
            self.conn.commit()

            createRequestTable = """CREATE TABLE IF NOT EXISTS requests (
                                                    chatID integer NOT NULL,
                                                    request text NOT NULL,
                                                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                                                );"""

            self.conn.execute(createRequestTable)
            self.conn.commit()

            createErrorTable = """CREATE TABLE IF NOT EXISTS errors (
                                                    ID integer PRIMARY KEY,
                                                    chatID integer NOT NULL,
                                                    request text NOT NULL,
                                                    error text NOT NULL,
                                                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                                                );"""

            self.conn.execute(createErrorTable)
            self.conn.commit()

        except Exception as e:
            print("DB :" + e)

    def updateLastRequest(self, chatID, request):
        update = """ INSERT OR REPLACE INTO lastRequest(chatID, request) VALUES(?,?); """
        self.conn.execute(update,(chatID,request))
        self.conn.commit()

    def drop(self):
        drop = """ DROP TABLE lastRequest;"""
        self.conn.execute(drop)
        self.conn.commit()

    def insertError(self, chatID, request, e):
        self.conn.execute("INSERT INTO errors(chatID, request, error, TIMESTAMP) VALUES( ?,?,?, DATETIME('now') );", (chatID, request, str(e)))
        self.conn.commit()


    def insertRequest(self, chatID, request):
        self.conn.execute("INSERT INTO requests VALUES( ?,?, DATETIME('now') );", (chatID, request))
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]