import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            kwargs["conn"] = conn
            return func(*args, **kwargs)            
        finally:
            if conn:
                conn.close()
    
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get("conn")
        if conn is None:
            raise ValueError("No DB connection found")
        try:
            # user_id = kwargs.get("user_id")
            # new_email = kwargs.get("new_email")
            result = func(*args, **kwargs)            
            conn.commit()
            return result
        except Exception as e:
            print(f"Exception occured and transaction rolling back {e}")
            if conn:
                conn.rollback()
            raise
    
    return wrapper

# Update user's email with automatic transaction handling 
@with_db_connection 
@transactional 
def update_user_email(user_id, new_email, conn=None): 
    if conn:
        cursor = conn.cursor() 
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
        return cursor.rowcount
        # cursor.execute("alter table users add email varchar(255)") 


rows = update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print(f"Rows affected: {rows}")

