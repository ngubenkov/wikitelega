import psycopg2

class DBHelper:

    def __init__(self):
        self.conn = psycopg2.connect(host="ec2-54-247-70-127.eu-west-1.compute.amazonaws.com",
                                    database="df7jrjh4gv153e", user="sqjmjpazjbvmrl", port = "5432",
                                    password="5c8e91b8f850ba76d1df21e24e4bf0daa0e12d4c3fb5f0ca2c1d1dd7e1a24ae1")


    def setup(self):
        createErrorTable = """CREATE TABLE IF NOT EXISTS errors (
                                                    ID SERIAL PRIMARY KEY,
                                                    chatID integer NOT NULL,
                                                    request text NOT NULL,
                                                    error text NOT NULL,
                                                    requested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                                                );"""

    # insert commands
    def insertRequest(self, chatID, request):
        self.cur = self.conn.cursor()
        insertQuerry = "INSERT INTO requests (chatid, request) VALUES (%s, %s);"
        data = (chatID, request,)
        self.cur.execute(insertQuerry, data)
        self.updateLastRequest(chatID, request)
        self.conn.commit()

    def insertError(self, chatID, request, e):
        self.cur = self.conn.cursor()
        insertSQL = "INSERT INTO errors (chatID, request, error) VALUES( %s, %s, %s);"
        data = (chatID, request, str(e),)
        self.cur.execute(insertSQL, data)
        self.conn.commit()
        self.cur.close()

    def add_item(self, item_text, owner):
        self.cur = self.conn.cursor()
        addSQL = "INSERT INTO items (description, owner) VALUES (%s, %s)"
        data = (item_text, owner, )
        self.cur.execute(addSQL, data)
        self.conn.commit()
        self.cur.close()

    # select commands
    def selectAll(self):  # select all requests
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM requests;")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        self.cur.close()

    def selectAllLast(self): # select last requests
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM lastRequest;")
        rows = self.cur.fetchall()
        info = ""
        for row in rows:
            info = info + str(row) + "\n"
        self.cur.close()
        return info

    def selectAllError(self): # select errors
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM errors;")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        self.cur.close()

    #other commands
    def updateLastRequest(self, chatID, request):
        self.cur = self.conn.cursor()
        update = """ INSERT INTO lastRequest(chatID, request) VALUES(%s, %s)
                        ON CONFLICT (chatID)   
                        DO 
                        UPDATE SET request = Excluded.request; """    # insert if not exist if exist (ON CONFLICT) update
        data = (chatID, request,)
        self.cur.execute(update, data)
        self.conn.commit()

    def drop(self):
        self.cur = self.conn.cursor()
        self.cur.execute("""DROP TABLE lastRequest;""")
        self.cur.commit()
        self.cur.close()


    def delete_item(self, item_text, owner):
        self.cur = self.conn.cursor()
        deleteSQL = "DELETE FROM items WHERE description = (%s) AND owner = (%s)"
        data = (item_text, owner, )
        self.cur.execute(deleteSQL, data)
        self.conn.commit()
        self.cur.close()

    def get_items(self, owner):
        self.cur = self.conn.cursor()
        getSQL = "SELECT description FROM items WHERE owner = (%)"
        data = (owner, )
        return [x[0] for x in self.cur.execute(getSQL, data)]


def main():
    db = DBHelper()
    #db.insertRequest('1','Inserted from local to heroku')
    #db.insertRequest('4', 'QQQQQqq')
    #db.insertRequest('5', 'WWWWW')
    #db.updateLastRequest(242215519, "updated")
    db.insertError(1,"errror", "errrrr")
    #print("########")
    db.selectAllError()
    #print(info)

if __name__ == '__main__':
    main()