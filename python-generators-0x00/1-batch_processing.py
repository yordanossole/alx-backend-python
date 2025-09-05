import seed

def stream_users_in_batches(batch_size):
    conn = seed.connect_to_prodev()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch


def batch_processing(batch_size): # processes each batch to filter users over the age of25`
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
