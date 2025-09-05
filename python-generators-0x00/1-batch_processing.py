import seed

def stream_users_in_batches(batch_size):
    conn = seed.connect_to_prodev()
    try:
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    except Exception as e:
            print(f"Error while streaming users: {e}")
            
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        


def batch_processing(batch_size): # processes each batch to filter users over the age of25`
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
