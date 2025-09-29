import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # default XAMPP MySQL user
        password="",          # default XAMPP MySQL password is empty
        database="fundi_sasa_db"
    )
