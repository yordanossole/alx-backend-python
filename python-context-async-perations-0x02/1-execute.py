import sqlite3

class ExecuteQuery():
    def __init__(self, path, query, param):
        self.path = path
        self.query = query
        self.param = (param, )
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.path)
            if self.conn:
                self.cursor = self.conn.cursor()
                if self.param:
                    self.cursor.execute(self.query, self.param)
                    rows = self.cursor.fetchall() 
                    return rows if rows else ["No user"]

                else:
                    self.cursor.execute(self.query)
                    rows = self.cursor.fetchall()
                    return rows if rows else ["No user"]

            else:
                raise ValueError("Unable to create DB connetion!")

        except Exception as e:
            print(f"Error: {e}")
            return ["Error..."]


    def __exit__(self, type, value, traceback):
        if self.cursor:
            self.cursor.close()
        
        if self.conn:
            if type is None:
                self.conn.commit()
                self.conn.close()
                print("Transaction commited and DB connection closed.")
            else:
                self.conn.rollback()
                self.conn.close()
                print("Transaction rolling back and DB connection closed.")
        

with ExecuteQuery("../python-decorators-0x01/users.db",
                   "SELECT * FROM users WHERE age > ?", 
                    "25") as rows:
    for row in rows:
        print(row)
