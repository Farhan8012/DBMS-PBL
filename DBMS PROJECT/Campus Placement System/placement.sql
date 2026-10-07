USE campus_placement;

-- Table 1: Students
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department VARCHAR(50),
    cgpa DECIMAL(4,2) CHECK (cgpa >= 0 AND cgpa <= 10.0),
    status ENUM('Unplaced', 'Placed') DEFAULT 'Unplaced'
);

-- Table 2: Companies
CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    hr_email VARCHAR(100) UNIQUE NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(255)
);

-- Table 3: Job Postings
CREATE TABLE job_postings (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    package_lpa DECIMAL(5,2),
    min_cgpa_required DECIMAL(4,2),
    deadline DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Table 4: Applications
-- This links Students to the Jobs they apply for
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    job_id INT,
    application_date DATE DEFAULT (CURRENT_DATE),
    status ENUM('Applied', 'Shortlisted', 'Rejected') DEFAULT 'Applied',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE
);

-- Table 5: Interviews
-- This tracks the interview rounds for shortlisted applications
CREATE TABLE interviews (
    interview_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT,
    interview_date DATETIME,
    interviewer_name VARCHAR(100),
    round_number INT DEFAULT 1,
    result ENUM('Pending', 'Selected', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER update_student_status
AFTER UPDATE ON interviews
FOR EACH ROW
BEGIN
    IF NEW.result = 'Selected' THEN
        UPDATE students 
        SET status = 'Placed' 
        WHERE student_id = (SELECT student_id FROM applications WHERE application_id = NEW.application_id);
    END IF;
END; //
DELIMITER ;

CREATE VIEW placement_summary AS
SELECT s.first_name, s.last_name, s.department, c.company_name, j.package_lpa
FROM interviews i
JOIN applications a ON i.application_id = a.application_id
JOIN students s ON a.student_id = s.student_id
JOIN job_postings j ON a.job_id = j.job_id
JOIN companies c ON j.company_id = c.company_id
WHERE i.result = 'Selected';