import seed
# from itertools import islice
    
    
def stream_users():
    conn = seed.connect_to_prodev()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data;")
        table = cursor.fetchall()
        for row in table:
            yield row

# for user in islice(stream_users(), 6):
#     print(user)