-- ==============================================================================
-- GyanPustak Seed Data (V10)
-- 
-- Description: Initial data injection for the frontend Streamlit application. 
--              This matches the exact data states hardcoded in the app.py 
--              initialization logic.
-- ==============================================================================

-- --------------------------------------------------------
-- 1. ACADEMIC INFRASTRUCTURE
-- --------------------------------------------------------

INSERT INTO Universities (name, address, rep_first_name, rep_last_name, rep_email, rep_phone)
VALUES 
('Tech University', '101 Campus Road', 'Robert', 'Oppenheimer', 'rob@tech.edu', '555-0101'),
('State College', '202 College Ave', 'Marie', 'Curie', 'marie@state.edu', '555-0202'),
('Global University', '303 Earth Blvd', 'Eve', 'Polastri', 'eve@global.edu', '555-0303'),
('National Institute', '404 Nation Way', 'Frank', 'Castle', 'frank@national.edu', '555-0404');

INSERT INTO Departments (name, university_id)
VALUES 
('Computer Science', 1), 
('Physics', 2), 
('Mathematics', 3), 
('Literature', 4);

INSERT INTO Courses (course_id, course_name, dept_id, university_id, year, semester)
VALUES 
('CS101', 'Intro to Databases', 1, 1, 2026, 'Fall'), 
('PHY201', 'Quantum Mechanics', 2, 2, 2026, 'Spring'),
('MAT301', 'Calculus III', 3, 3, 2026, 'Fall'), 
('LIT101', 'Classic Literature', 4, 4, 2026, 'Spring');

-- --------------------------------------------------------
-- 2. USERS (STUDENTS, EMPLOYEES & INSTRUCTORS)
-- --------------------------------------------------------

INSERT INTO Students (first_name, last_name, email, password, address, phone, dob, university_id, major, student_status, year_of_study)
VALUES 
('John', 'Doe', 'john.doe@email.com', 'student123', 'Apt 4B, City Center', '1234567890', '2003-05-12', 1, 'Software Engineering', 'undergraduate', '3rd'),
('Jane', 'Smith', 'jane.smith@email.com', 'student123', 'Dorm 2, State Campus', '0987654321', '2001-11-23', 2, 'Applied Physics', 'graduate', '1st'),
('Alice', 'Wonderland', 'alice@email.com', 'student123', '789 Rabbit Hole', '1112223333', '2004-04-01', 3, 'Mathematics', 'undergraduate', '2nd'),
('Bob', 'Builder', 'bob@email.com', 'student123', '101 Construction Way', '4445556666', '2002-09-15', 4, 'Civil Engineering', 'graduate', '1st');

INSERT INTO Employees (role, first_name, last_name, gender, password, salary, aadhaar_number, email, address, phone)
VALUES 
('Super Administrator', 'Alan', 'Turing', 'Male', 'super123', 120000.00, '[Redacted]1', 'alan.super@gyan.com', 'HQ Building', '555-9999'),
('Administrator', 'Grace', 'Hopper', 'Female', 'admin123', 90000.00, '[Redacted]2', 'grace.admin@gyan.com', 'Admin Block', '555-7777'),
('Customer Support', 'Ada', 'Lovelace', 'Female', 'support123', 65000.00, '[Redacted]3', 'ada.support@gyan.com', 'Support Center', '555-8888'),
('Administrator', 'Charlie', 'Chaplin', 'Male', 'admin123', 85000.00, '[Redacted]4', 'charlie.admin@gyan.com', 'Comedy St', '555-4444'),
('Customer Support', 'Diana', 'Prince', 'Female', 'support123', 68000.00, '[Redacted]5', 'diana.support@gyan.com', 'Themyscira', '555-5555');

INSERT INTO Instructors (first_name, last_name, university_id, dept_id)
VALUES 
('Dr. Grace', 'Hopper', 1, 1), 
('Dr. Richard', 'Feynman', 2, 2), 
('Dr. Isaac', 'Newton', 3, 3), 
('Dr. Mark', 'Twain', 4, 4);

INSERT INTO Course_Instructors (course_id, instructor_id)
VALUES 
('CS101', 1), ('PHY201', 2), ('MAT301', 3), ('LIT101', 4);

-- --------------------------------------------------------
-- 3. FRONTEND INVENTORY (BOOKS, AUTHORS, KEYWORDS)
-- --------------------------------------------------------

INSERT INTO Books (isbn, title, type, price, quantity, publisher, publication_date, edition_number, language, format, category, subcategory)
VALUES 
('978-013', 'Database System Concepts', 'new', 1500.00, 50, 'McGraw Hill', '2020-03-01', '7th', 'English', 'hardcover', 'Computer Science', 'Databases'),
('978-045', 'Feynman Lectures on Physics', 'used', 450.00, 20, 'Basic Books', '2011-10-04', 'New', 'English', 'softcover', 'Science', 'Physics'),
('978-099', 'Calculus Early Transcendentals', 'new', 2000.00, 40, 'Cengage', '2021-01-01', '9th', 'English', 'hardcover', 'Mathematics', 'Calculus'),
('978-111', 'Adventures of Huckleberry Finn', 'used', 300.00, 15, 'Penguin', '2010-05-05', 'Reprint', 'English', 'softcover', 'Literature', 'Fiction');

INSERT INTO Book_Authors (isbn, author_name) 
VALUES 
('978-013', 'Abraham Silberschatz'), 
('978-045', 'Richard P. Feynman'), 
('978-099', 'James Stewart'), 
('978-111', 'Mark Twain');
                   
INSERT INTO Book_Keywords (isbn, keyword) 
VALUES 
('978-013', 'SQL'), 
('978-045', 'Mechanics'), 
('978-099', 'Math'), 
('978-111', 'Novel');
                   
INSERT INTO Course_Books (course_id, isbn, req_type) 
VALUES 
('CS101', '978-013', 'required'), 
('PHY201', '978-045', 'recommended'), 
('MAT301', '978-099', 'required'), 
('LIT101', '978-111', 'recommended');

INSERT INTO Book_Reviews (student_id, isbn, rating, review_text, review_date)
VALUES 
(1, '978-013', 5, 'Heavy but very detailed.', '2026-04-01 14:00:00'),
(2, '978-045', 4, 'Great concepts, hard math.', '2026-04-05 09:30:00');

-- --------------------------------------------------------
-- 4. E-COMMERCE (CARTS & ORDERS)
-- --------------------------------------------------------

INSERT INTO Cart (student_id, date_created, date_last_updated) 
VALUES 
(1, '2026-04-12 10:00:00', '2026-04-12 10:05:00'), 
(2, '2026-04-12 11:00:00', '2026-04-12 11:05:00'),
(3, '2026-04-12 12:00:00', '2026-04-12 12:05:00'), 
(4, '2026-04-12 13:00:00', '2026-04-12 13:05:00');
                   
INSERT INTO Cart_Books (cart_id, isbn, quantity, purchase_type) 
VALUES 
(1, '978-013', 1, 'Buy'), 
(2, '978-045', 2, 'Rent'), 
(3, '978-099', 1, 'Buy'), 
(4, '978-111', 2, 'Rent');

INSERT INTO Orders (student_id, date_created, date_fulfilled, shipping_type, cc_number, cc_exp_date, cc_holder_name, cc_type, status)
VALUES 
(1, '2026-04-10 09:00:00', '2026-04-11 14:00:00', '2-day', '1111222233334444', '12/28', 'John Doe', 'Visa', 'shipped'),
(2, '2026-04-11 15:30:00', NULL, 'standard', '5555666677778888', '11/27', 'Jane Smith', 'MasterCard', 'processed'),
(3, '2026-04-09 10:00:00', '2026-04-10 14:00:00', '1-day', '4444555566667777', '09/29', 'Alice Wonderland', 'Visa', 'shipped'),
(4, '2026-04-08 11:00:00', NULL, 'standard', '8888999900001111', '05/25', 'Bob Builder', 'Amex', 'new');
                   
INSERT INTO Order_Books (order_id, isbn, quantity, purchase_price, purchase_type) 
VALUES 
(1, '978-013', 1, 1500.00, 'Buy'), 
(2, '978-045', 1, 450.00, 'Rent'), 
(3, '978-099', 1, 2000.00, 'Buy'), 
(4, '978-111', 1, 300.00, 'Rent');

-- --------------------------------------------------------
-- 5. TICKETING SYSTEM
-- --------------------------------------------------------

INSERT INTO Trouble_Tickets (category, date_logged, created_by_student_id, created_by_emp_id, title, problem_description, solution_description, completion_date, status, resolved_by_admin_id)
VALUES 
('cart', '2026-04-12 08:00:00', 1, NULL, 'Cannot add second book', 'The cart throws an error when adding book 2', NULL, NULL, 'new', NULL),
('orders', '2026-04-11 10:00:00', 2, NULL, 'Tracking number missing', 'My order says shipped but no tracking', 'Emailed tracking number', '2026-04-12 09:00:00', 'completed', 1),
('user profile', '2026-04-12 09:00:00', 3, NULL, 'Cannot update address', 'Address field is locked', NULL, NULL, 'assigned', NULL),
('products', '2026-04-12 10:00:00', NULL, 3, 'Book image missing', 'Huckleberry Finn book has no cover image', 'Re-uploaded image', '2026-04-12 11:00:00', 'completed', 2);
