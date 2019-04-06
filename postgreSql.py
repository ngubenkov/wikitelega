import psycopg2

class DBHelper:

    def __init__(self):
        self.conn = psycopg2.connect(host="ec2-54-75-245-196.eu-west-1.compute.amazonaws.com",
                                   database="d6jl5hpm0h81ta", user="subhmwvwkczboo", port="5432",
                                   password="65dba2994e5e08ef80dbc1ae8275ca9abcd38af2d04cb830a2bb24171da45bad")


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
        self.cur.callproc('inser_request', [chatID, request,])

    def insertError(self, chatID, request, e):  # done
        self.cur = self.conn.cursor()
        self.cur.callproc('insert_error', [chatID, request, e,])

    # select commands
    def selectAll(self):  # select all requests
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM requests;")
        rows = self.cur.fetchall()
        info = ""
        for row in rows:
            print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
            info = info + str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "\n"
        self.cur.close()
        return info

    def selectAllLast(self): # select last requests
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM lastRequest;")
        rows = self.cur.fetchall()
        info = ""
        for row in rows:
            print(row)
            info = info + str(row[0]) + " " + str(row[1]) + "\n"
        self.cur.close()
        return info

    def selectAllError(self): # select errors
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM errors;")
        rows = self.cur.fetchall()
        info = ""
        for row in rows:
            #print(row)
            print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]))
            info = info + str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + "\n"
        self.cur.close()
        return info

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
        getSQL = "SELECT description FROM items WHERE owner = %s"
        data = (owner, )
        return [x[0] for x in self.cur.execute(getSQL, data)]


def main():
    #db.insertRequest('1','Inserted from local to heroku')
    #db.insertRequest('4', 'QQQQQqq')
    #db.insertRequest('5', 'WWWWW')
    #db.updateLastRequest(242215519, "updated")
    #db.insertError(1,"errror", "errrrr")
    #print("########")
    #db.selectAllLast()
    #print(info)

    db = DBHelper()
    db.insertError(44, 'testing test', 'testing')
    db.selectAllError()

if __name__ == '__main__':
    main()