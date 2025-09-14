import time
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if query_cache:
            result = query_cache.get(kwargs['query'])
            print(f"From cache: {query_cache}")
            return result
        else:
            result = func(*args, **kwargs)
            query_cache[kwargs["query"]] = result
            return result
    
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(query, conn=None):
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

#### First call will cache the result
print("users:")
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
print("users_again:")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

print("users_again 2nd:")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

