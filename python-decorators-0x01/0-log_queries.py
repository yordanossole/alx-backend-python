import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get('query')
        print(f"[Log] SQL Query: {query}")
        print(f"[Log] Function: {func.__name__}")
        print(f"[Log] Args: {args}, Kwargs: {kwargs}")
        start_time = datetime.now()

        try:
            result = func(*args, **kwargs)
            elapsed = datetime.now() - start_time
            print(f"[Log] Execution time: {elapsed}s")
            print(f"[Log] Rows returned: {len(result) if result else 0}")
            return result
        except Exception as e:
            print(f"[Log] Error failed: {e}")

    return wrapper

#  """ YOUR CODE GOES HERE"""
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users;")
# users = fetch_all_users("create table users(id int, name varchar(255), age int)")
