from db import get_db_connection

def add_student(conn):
    cursor = conn.cursor()
    print("\n--- Add New Student ---")
    student_id = input("Enter Student ID (e.g., STU001): ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")
    
    try:
        cgpa = float(input("Enter CGPA (0.0 to 10.0): "))
        
        # SQL query to insert data
        query = """
        INSERT INTO students (student_id, first_name, last_name, email, department, cgpa)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (student_id, first_name, last_name, email, department, cgpa)
        
        cursor.execute(query, values)
        conn.commit() # This saves the changes to the database
        print(f"✅ Student {first_name} {last_name} added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding student: {e}")
    finally:
        cursor.close()

def view_students(conn):
    cursor = conn.cursor()
    print("\n--- Student List ---")
    query = "SELECT student_id, first_name, last_name, department, cgpa, status FROM students"
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        if not records:
            print("No students found in the database.")
        else:
            for row in records:
                # row[0] is student_id, row[1] is first_name, etc.
                print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Dept: {row[3]} | CGPA: {row[4]} | Status: {row[5]}")
                
    except Exception as e:
        print(f"❌ Error retrieving students: {e}")
    finally:
        cursor.close()




def add_company(conn):
    cursor = conn.cursor()
    print("\n--- Add New Company ---")
    company_name = input("Enter Company Name: ")
    hr_email = input("Enter HR Email: ")
    industry = input("Enter Industry (e.g., IT, Finance): ")
    
    try:
        # Note: company_id is AUTO_INCREMENT, so we don't insert it manually
        query = """
        INSERT INTO companies (company_name, hr_email, industry)
        VALUES (%s, %s, %s)
        """
        values = (company_name, hr_email, industry)
        
        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Company {company_name} added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding company: {e}")
    finally:
        cursor.close()

def view_companies(conn):
    cursor = conn.cursor()
    print("\n--- Company List ---")
    query = "SELECT company_id, company_name, hr_email, industry FROM companies"
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        if not records:
            print("No companies found in the database.")
        else:
            for row in records:
                print(f"ID: {row[0]} | Name: {row[1]} | HR: {row[2]} | Industry: {row[3]}")
                
    except Exception as e:
        print(f"❌ Error retrieving companies: {e}")
    finally:
        cursor.close()

def main():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database. Exiting...")
        return

    while True:
        print("\n" + "="*30)
        print(" CAMPUS PLACEMENT SYSTEM ")
        print("="*30)
        print("1. Add a New Student")
        print("2. View All Students")
        print("3. Add a New Company")
        print("4. View All Companies")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_student(conn)
        elif choice == '2':
            view_students(conn)
        elif choice == '3':
            add_company(conn)
        elif choice == '4':
            view_companies(conn)
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
    conn.close()

if __name__ == "__main__":
    main()