import os
import mysql.connector
from mysql.connector import Error

# Default connection parameters
DEFAULT_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Farhan@123"),
    "database": os.getenv("DB_NAME", "campus_placement"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_db_connection(host=None, user=None, password=None, database=None, port=None):
    """
    Returns a MySQL database connection.
    Falls back to environment variables or DEFAULT_CONFIG if arguments are not provided.
    """
    try:
        connection = mysql.connector.connect(
            host=host or DEFAULT_CONFIG["host"],
            user=user or DEFAULT_CONFIG["user"],
            password=password if password is not None else DEFAULT_CONFIG["password"],
            database=database or DEFAULT_CONFIG["database"],
            port=port or DEFAULT_CONFIG["port"],
            autocommit=True
        )
        return connection
    except Error as err:
        print(f"Database Connection Error: {err}")
        return None

def test_db_connection(host=None, user=None, password=None, database=None, port=None):
    """
    Tests the connection and returns a tuple (is_successful, message).
    """
    try:
        conn = get_db_connection(host, user, password, database, port)
        if conn and conn.is_connected():
            server_info = getattr(conn, 'server_info', '8.0+')
            conn.close()
            return True, f"Connected to MySQL {server_info} successfully!"
        return False, "Failed to connect to database."
    except Error as e:
        return False, str(e)

def init_db_schema(conn=None):
    """
    Ensures that the trigger and view defined in placement.sql are created.
    """
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        
        # Ensure trigger exists
        cursor.execute("SHOW TRIGGERS WHERE `Trigger` = 'update_student_status'")
        if not cursor.fetchall():
            cursor.execute("""
            CREATE TRIGGER update_student_status
            AFTER UPDATE ON interviews
            FOR EACH ROW
            BEGIN
                IF NEW.result = 'Selected' THEN
                    UPDATE students 
                    SET status = 'Placed' 
                    WHERE student_id = (SELECT student_id FROM applications WHERE application_id = NEW.application_id);
                END IF;
            END;
            """)

        # Ensure view exists
        cursor.execute("""
        CREATE OR REPLACE VIEW placement_summary AS
        SELECT s.first_name, s.last_name, s.department, c.company_name, j.package_lpa
        FROM interviews i
        JOIN applications a ON i.application_id = a.application_id
        JOIN students s ON a.student_id = s.student_id
        JOIN job_postings j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE i.result = 'Selected';
        """)
        
        cursor.close()
        if should_close:
            conn.close()
        return True, "Database schema verified."
    except Exception as e:
        if should_close and conn:
            conn.close()
        return False, str(e)

# Test the connection
if __name__ == "__main__":
    success, msg = test_db_connection()
    if success:
        print(f"[OK] {msg}")
        init_db_schema()
    else:
        print(f"[FAIL] {msg}")
