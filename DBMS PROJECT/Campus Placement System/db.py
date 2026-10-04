import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username if different
            password="Farhan@123",  # Replace with your actual MySQL password
            database="campus_placement"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Test the connection
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Successfully connected to the database!")
        conn.close()