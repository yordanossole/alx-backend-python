import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            user_id = kwargs.get("user_id")
            user = func(user_id, conn) if user_id else ""
            return user
        finally:
            if conn:
                conn.close()
    
    return wrapper
        
                
# Fetch user by ID with automatic connection handling 
@with_db_connection 
def get_user_by_id(user_id, conn=None): 
    cursor = None
    try:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
            return cursor.fetchone() 
    finally:
        if cursor:
            cursor.close()


user = get_user_by_id(user_id=1)
print(user)