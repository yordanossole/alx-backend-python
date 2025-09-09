import sqlite3
class DatabaseConnection():
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None
        

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.path)
            if self.conn:
                self.cursor = self.conn.cursor()
                return self.cursor
            else:
                raise ValueError("Unable to create DB connetion!")
        except Exception as e:
            print(f"Error: {e}")
        

    def __exit__(self, type, value, traceback):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")

        if self.conn:
            if type is None:
                self.conn.commit()
                self.conn.close()
                print("Transaction commited and DB connection closed.")
            else:
                self.conn.rollback()
                self.conn.close()
                print("Transaction rolling back and DB connection closed.")


with DatabaseConnection('../python-decorators-0x01/users.db') as cursor:
    query = "SELECT * FROM users"
    rows = []
    
    if cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    for row in rows:
        print(row)