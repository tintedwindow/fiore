import sqlite3

# creates the database
connection = sqlite3.connect('fiore.db')
cursor = connection.cursor()

# schema commands
create_table_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        username TEXT UNIQUE NOT NULL, 
        hash TEXT NOT NULL, 
        creation_date DATE NOT NULL
    );
"""
create_table_images = """
    CREATE TABLE IF NOT EXISTS images ( 
        image_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER, 
        filename TEXT NOT NULL, 
        image_date DATE NOT NULL, 
        description TEXT, 
        upload_date DATE NOT NULL, 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, 
        UNIQUE (user_id, image_date)
    );
"""
# executing the commands
cursor.execute(create_table_users)
cursor.execute(create_table_images)
# commiting the changes
connection.commit()
# closing the connection
connection.close()
print("Database created succesfully. Please proceed with running Fiore via 'flask run'")
    