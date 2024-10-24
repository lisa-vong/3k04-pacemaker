import sqlite3

# Creating database file if not already exists
def create_db(dbName="users.db"):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL  
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            parameter TEXT NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
    conn.commit()
    conn.close()
    
#registration validation and adds inputs to database
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    #checks number of users in database and returns error if there is 10 already
    cursor.execute("SELECT COUNT (*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count >= 10:
        conn.close()
        return False, "Maximum number of users reached. Cannot register more than 10 users!"
    
    #checks if username already exists in database otherwise adds user info to database
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return False, "Error, username already exists!"
    
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    
    conn.commit()
    conn.close()
    return True, "Success, user registered!"

#checks if login inputs match data in database
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    return user is not None, user[0] if user else None