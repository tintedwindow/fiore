import os
import sqlite3

if not os.path.exists('fiore.db'):
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
        CREATE TABLE images ( 
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
    cursor.execute(create_table_sql)
    # Commit the changes
    connection.commit()
    # Close the connection
    connection.close()

else:
    print("Database already exists. Please proceed with running Fiore via 'flask run'")