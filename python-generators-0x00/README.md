# Python MySQL Seeder

This project provides a Python script to set up a MySQL database, create a table, and populate it with sample data from a CSV file. It is designed for learning how to interact with MySQL databases using Python.

## Project Structure

```
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py           # Main script to set up the database and seed data
    ├── user_data.csv     # CSV file containing sample user data
    └── 0-main.py         # Script to test the seed.py functionality
```

## Requirements

* Python 3.x
* MySQL server running locally
* `mysql-connector-python` library

Install the MySQL connector using:

```bash
pip install mysql-connector-python
```

## Database Setup

The script will:

1. Connect to the MySQL server.
2. Create a database called `ALX_prodev` if it does not exist.
3. Create a table `user_data` with the following fields:

| Field    | Type    | Constraints          |
| -------- | ------- | -------------------- |
| user\_id | UUID    | Primary Key, Indexed |
| name     | VARCHAR | NOT NULL             |
| email    | VARCHAR | NOT NULL             |
| age      | DECIMAL | NOT NULL             |

4. Populate the table with data from `user_data.csv`.

## Function Prototypes in `seed.py`

* `connect_db()`: Connects to the MySQL server.
* `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
* `connect_to_prodev()`: Connects specifically to the `ALX_prodev` database.
* `create_table(connection)`: Creates the `user_data` table if it does not exist.
* `insert_data(connection, data)`: Inserts data from CSV into the `user_data` table if it does not already exist.

## Usage

Run the `0-main.py` script to set up the database and populate data:

```bash
python main.py
```

Expected output:

```
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

This confirms that the database and table were created successfully, and sample data was inserted.

## Author

**Yordanos Solomon**

---

If you want, I can also draft a **more beginner-friendly version** with diagrams showing how the CSV data flows into MySQL. It can make your README stand out in the repo. Do you want me to do that?
