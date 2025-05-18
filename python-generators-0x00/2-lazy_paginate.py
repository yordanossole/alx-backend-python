["def paginate_users", "SELECT * FROM user_data LIMIT", "OFFSET"]
["paginate_users(page_size, offset)"]

def lazy_paginate(page_size):
    return