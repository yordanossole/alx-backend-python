# import time
# import sqlite3 
# import functools

#### paste your with_db_decorator here

""" your code goes here"""
def with_db_connection():
    pass
def retry_on_failure(retries=3, delay=1):
    pass

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)