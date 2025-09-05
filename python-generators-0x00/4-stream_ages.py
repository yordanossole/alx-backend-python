import seed

# generator
def stream_user_ages():
    conn = None
    cursor = None
    
    try:
        conn = seed.connect_to_prodev()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT age FROM user_data;")
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                yield row
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def calculate_average_age():
    counter = 0
    total = 0
    for age in stream_user_ages():
        counter += 1
        total += age["age"]
    print(f"Average age of users: {total/counter}")

calculate_average_age()