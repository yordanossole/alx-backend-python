from mysql.connector import connect
import mysql.connector
import csv

def connect_db() : # connects to the mysql database server 
    try:
        conn = connect(
            host="localhost",
            user="admin",
            password="admin",
        )
        print("Database connected successfuly.")
        return conn
    
    except mysql.connector.Error as e:
        print(f"Error occured: {e}")
        return None


def create_database(connection):#- creates the database ALX_prodev if it does not exist
    cursor = None
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE ALX_prodev;")
            print("Database created successfuly.")
    except Exception:
        print("Database already created!")
    finally:
        if cursor:
            cursor.close()
        # if connection and connection.is_connected():
        #     connection.close()

        

def connect_to_prodev(): # connects the the ALX_prodev database in MYSQL
    try:
        conn = connect(
            host="localhost",
            user="admin",
            password="admin",
            database="ALX_prodev"
        )
        print("Database connected successfuly to ALX_prodev")
        return conn
    except Exception:
        print("Error occured")
        return None
    

def create_table(connection):#- creates a table user_data if it does not exists with the required fields
    cursor = None
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE user_data 
                           (user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
                           name VARCHAR(255) NOT NULL,
                           email VARCHAR(255) NOT NULL,
                           age DECIMAL NOT NULL);''')
            print("Table created successfuly.")
    except Exception:
        print("Table already exists!")
    finally:
        if cursor:
            cursor.close()
        # if connection and connection.is_connected():
        #     connection.close()


def insert_data(connection, data): #- inserts data in the database if it does not exist

    with open(data, "r") as file_handle:
        file_reader = csv.reader(file_handle)
        next(file_reader)
        rows = [(row[0], row[1], int(row[2])) for row in file_reader]


    cursor = None
    try:
        if connection:
            cursor = connection.cursor()
            query = '''INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s);'''
            cursor.executemany(query, rows)
            connection.commit()
            print("Data inserted successfuly.")
        else:
            print("no connection")
    except Exception as e:
        print(f"Error occured while inserting data! {e}")
    finally:
        if cursor:
            cursor.close()
        # if connection and connection.is_connected():
        #     connection.close()
    


# normal_conn = connect_db()

# create_database(normal_conn)
# prodev_con = connect_to_prodev()
# create_table(prodev_con)
# prodev_con = connect_to_prodev()
# insert_data(prodev_con, "user_data.csv")



