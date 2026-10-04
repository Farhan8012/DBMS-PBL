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


def add_job_posting(conn):
    cursor = conn.cursor()
    print("\n--- Add New Job Posting ---")
    
    # Show available companies first so the user knows which ID to pick
    try:
        cursor.execute("SELECT company_id, company_name FROM companies")
        companies = cursor.fetchall()
        if not companies:
            print("⚠️ No companies found! Please add a company first.")
            return
            
        print("Available Companies:")
        for row in companies:
            print(f"  ID: {row[0]} - {row[1]}")
            
        company_id = int(input("\nEnter Company ID from the list above: "))
        job_title = input("Enter Job Title (e.g., Software Engineer): ")
        package_lpa = float(input("Enter Package (LPA): "))
        min_cgpa = float(input("Enter Minimum CGPA Required: "))
        deadline = input("Enter Deadline (YYYY-MM-DD): ")
        
        query = """
        INSERT INTO job_postings (company_id, job_title, package_lpa, min_cgpa_required, deadline)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (company_id, job_title, package_lpa, min_cgpa, deadline)
        
        cursor.execute(query, values)
        conn.commit()
        print(f"✅ Job '{job_title}' added successfully!")
        
    except ValueError:
        print("❌ Invalid input! Package and CGPA must be numbers.")
    except Exception as e:
        print(f"❌ Error adding job posting: {e}")
    finally:
        cursor.close()

def view_job_postings(conn):
    cursor = conn.cursor()
    print("\n--- Job Postings List ---")
    
    # Using a JOIN to get the actual company name instead of just the company_id
    query = """
    SELECT j.job_id, c.company_name, j.job_title, j.package_lpa, j.min_cgpa_required, j.deadline 
    FROM job_postings j
    JOIN companies c ON j.company_id = c.company_id
    """
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        if not records:
            print("No job postings found in the database.")
        else:
            for row in records:
                print(f"Job ID: {row[0]} | Company: {row[1]} | Role: {row[2]} | Package: {row[3]} LPA | Min CGPA: {row[4]} | Deadline: {row[5]}")
                
    except Exception as e:
        print(f"❌ Error retrieving job postings: {e}")
    finally:
        cursor.close()

def add_application(conn):
    cursor = conn.cursor()
    print("\n--- Add New Application ---")
    
    try:
        # 1. Show available students
        cursor.execute("SELECT student_id, first_name, last_name FROM students")
        students = cursor.fetchall()
        if not students:
            print("⚠️ No students found! Please add a student first.")
            return
            
        print("Available Students:")
        for s in students:
            print(f"  ID: {s[0]} - {s[1]} {s[2]}")
            
        # 2. Show available jobs
        cursor.execute("""
            SELECT j.job_id, c.company_name, j.job_title 
            FROM job_postings j 
            JOIN companies c ON j.company_id = c.company_id
        """)
        jobs = cursor.fetchall()
        if not jobs:
            print("⚠️ No jobs found! Please add a job first.")
            return
            
        print("\nAvailable Jobs:")
        for j in jobs:
            print(f"  Job ID: {j[0]} - {j[1]} ({j[2]})")
            
        # 3. Get input and insert
        student_id = input("\nEnter Student ID from the list above: ")
        job_id = int(input("Enter Job ID from the list above: "))
        
        query = """
        INSERT INTO applications (student_id, job_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (student_id, job_id))
        conn.commit()
        print("✅ Application submitted successfully!")
        
    except ValueError:
        print("❌ Invalid input! Job ID must be a number.")
    except Exception as e:
        print(f"❌ Error adding application: {e}")
    finally:
        cursor.close()

def view_applications(conn):
    cursor = conn.cursor()
    print("\n--- Applications List ---")
    
    # Joining 4 tables to get a complete readable report
    query = """
    SELECT a.application_id, s.first_name, s.last_name, c.company_name, j.job_title, a.status, a.application_date
    FROM applications a
    JOIN students s ON a.student_id = s.student_id
    JOIN job_postings j ON a.job_id = j.job_id
    JOIN companies c ON j.company_id = c.company_id
    """
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        if not records:
            print("No applications found in the database.")
        else:
            for row in records:
                print(f"App ID: {row[0]} | Student: {row[1]} {row[2]} | Company: {row[3]} | Role: {row[4]} | Status: {row[5]} | Date: {row[6]}")
                
    except Exception as e:
        print(f"❌ Error retrieving applications: {e}")
    finally:
        cursor.close()

def add_interview(conn):
    cursor = conn.cursor()
    print("\n--- Schedule New Interview ---")
    
    try:
        # Show pending applications
        cursor.execute("""
            SELECT a.application_id, s.first_name, s.last_name, c.company_name, j.job_title 
            FROM applications a
            JOIN students s ON a.student_id = s.student_id
            JOIN job_postings j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
        """)
        apps = cursor.fetchall()
        
        if not apps:
            print("⚠️ No applications found! Please add an application first.")
            return
            
        print("Current Applications:")
        for a in apps:
            print(f"  App ID: {a[0]} | Student: {a[1]} {a[2]} | Company: {a[3]} ({a[4]})")
            
        app_id = int(input("\nEnter Application ID from the list above: "))
        interview_date = input("Enter Interview Date & Time (YYYY-MM-DD HH:MM:SS): ")
        interviewer = input("Enter Interviewer Name: ")
        round_num = int(input("Enter Round Number (e.g., 1 for Technical, 2 for HR): "))
        result = input("Enter Result (Pending, Selected, Rejected): ")
        
        query = """
        INSERT INTO interviews (application_id, interview_date, interviewer_name, round_number, result)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (app_id, interview_date, interviewer, round_num, result))
        conn.commit()
        print("✅ Interview scheduled successfully!")
        
    except ValueError:
        print("❌ Invalid input! Application ID and Round Number must be numbers.")
    except Exception as e:
        print(f"❌ Error scheduling interview: {e}")
    finally:
        cursor.close()

def view_interviews(conn):
    cursor = conn.cursor()
    print("\n--- Interview Schedule & Results ---")
    
    # 5-table JOIN to show a complete, readable interview report
    query = """
    SELECT i.interview_id, s.first_name, s.last_name, c.company_name, 
           j.job_title, i.round_number, i.interview_date, i.result
    FROM interviews i
    JOIN applications a ON i.application_id = a.application_id
    JOIN students s ON a.student_id = s.student_id
    JOIN job_postings j ON a.job_id = j.job_id
    JOIN companies c ON j.company_id = c.company_id
    """
    
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        
        if not records:
            print("No interviews scheduled yet.")
        else:
            for row in records:
                print(f"Int ID: {row[0]} | Candidate: {row[1]} {row[2]} | Company: {row[3]} - {row[4]} | Round: {row[5]} | Date: {row[6]} | Status: {row[7]}")
                
    except Exception as e:
        print(f"❌ Error retrieving interviews: {e}")
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
        print("5. Add a New Job Posting")
        print("6. View All Job Postings")
        print("7. Add a New Application")
        print("8. View All Applications")
        print("9. Schedule an Interview")
        print("10. View All Interviews")
        print("11. Exit")
        
        choice = input("Enter your choice (1-11): ")
        
        if choice == '1':
            add_student(conn)
        elif choice == '2':
            view_students(conn)
        elif choice == '3':
            add_company(conn)
        elif choice == '4':
            view_companies(conn)
        elif choice == '5':
            add_job_posting(conn)
        elif choice == '6':
            view_job_postings(conn)
        elif choice == '7':
            add_application(conn)
        elif choice == '8':
            view_applications(conn)
        elif choice == '9':
            add_interview(conn)
        elif choice == '10':
            view_interviews(conn)
        elif choice == '11':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
    conn.close()

if __name__ == "__main__":
    main()