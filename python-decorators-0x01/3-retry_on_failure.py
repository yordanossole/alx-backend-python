import time
import sqlite3 
import functools

def with_db_connection(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            kwargs['conn'] = conn
            users = func(*args, **kwargs)
            return users
        finally:
            if conn:
                conn.close()
    
    return wrapper

def retry_on_failure(retries, delay):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):            
            conn = kwargs.get('conn')
            if not conn:
                raise ValueError("No DB connection found.")
            nonlocal retries
            while retries > 0:
                try:
                    retries -= 1
                    users = func(conn)
                    ## Test whether it handles or not
                    # if retries >= 1:
                    #     raise ValueError("test error")
                    return users
                except Exception as e:
                    time.sleep(delay)            
                    print(f"Error: {e}")
            else:
                print("All retries failed")                  

        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn=None):
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()


# attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)