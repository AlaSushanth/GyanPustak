-- ==============================================================================
-- GyanPustak Master Database Schema (V10)
-- 
-- Description: DDL scripts to generate the normalized 18-table relational 
--              database for the GyanPustak textbook rental/purchase platform.
-- Engine:      SQLite3
-- ==============================================================================

-- --------------------------------------------------------
-- 1. ACADEMIC ORGANIZATION TABLES
-- --------------------------------------------------------

CREATE TABLE Universities (
    university_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT UNIQUE NOT NULL, 
    address TEXT, 
    rep_first_name TEXT, 
    rep_last_name TEXT, 
    rep_email TEXT, 
    rep_phone TEXT
);

CREATE TABLE Departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    university_id INTEGER, 
    FOREIGN KEY (university_id) REFERENCES Universities(university_id)
);

CREATE TABLE Courses (
    course_id TEXT PRIMARY KEY, 
    course_name TEXT, 
    dept_id INTEGER, 
    university_id INTEGER, 
    year INTEGER, 
    semester TEXT,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id),
    FOREIGN KEY (university_id) REFERENCES Universities(university_id)
);

CREATE TABLE Instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT, 
    last_name TEXT, 
    university_id INTEGER, 
    dept_id INTEGER,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id),
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Course_Instructors (
    course_id TEXT, 
    instructor_id INTEGER, 
    PRIMARY KEY (course_id, instructor_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)
);

-- --------------------------------------------------------
-- 2. USER & AUTHENTICATION TABLES
-- --------------------------------------------------------

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT, 
    last_name TEXT, 
    email TEXT UNIQUE, 
    password TEXT NOT NULL, 
    address TEXT, 
    phone TEXT, 
    dob TEXT, 
    university_id INTEGER, 
    major TEXT, 
    student_status TEXT, 
    year_of_study TEXT,
    FOREIGN KEY (university_id) REFERENCES Universities(university_id)
);

CREATE TABLE Employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    role TEXT, 
    first_name TEXT, 
    last_name TEXT, 
    gender TEXT, 
    password TEXT NOT NULL, 
    salary REAL, 
    aadhaar_number TEXT UNIQUE, 
    email TEXT UNIQUE, 
    address TEXT, 
    phone TEXT
);

-- --------------------------------------------------------
-- 3. INVENTORY & BOOK MASTER TABLES
-- --------------------------------------------------------

CREATE TABLE Books (
    isbn TEXT PRIMARY KEY, 
    title TEXT, 
    type TEXT, 
    price REAL, 
    quantity INTEGER, 
    publisher TEXT, 
    publication_date TEXT, 
    edition_number TEXT, 
    language TEXT, 
    format TEXT, 
    category TEXT, 
    subcategory TEXT
);

CREATE TABLE Book_Authors (
    isbn TEXT, 
    author_name TEXT, 
    PRIMARY KEY (isbn, author_name),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

CREATE TABLE Book_Keywords (
    isbn TEXT, 
    keyword TEXT, 
    PRIMARY KEY (isbn, keyword),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

CREATE TABLE Course_Books (
    course_id TEXT, 
    isbn TEXT, 
    req_type TEXT, 
    PRIMARY KEY (course_id, isbn),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

CREATE TABLE Book_Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    student_id INTEGER, 
    isbn TEXT, 
    rating INTEGER, 
    review_text TEXT, 
    review_date TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

-- --------------------------------------------------------
-- 4. E-COMMERCE & FULFILLMENT TABLES
-- --------------------------------------------------------

CREATE TABLE Cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    student_id INTEGER UNIQUE, 
    date_created TEXT, 
    date_last_updated TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

CREATE TABLE Cart_Books (
    cart_id INTEGER, 
    isbn TEXT, 
    quantity INTEGER, 
    purchase_type TEXT, 
    PRIMARY KEY (cart_id, isbn),
    FOREIGN KEY (cart_id) REFERENCES Cart(cart_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    student_id INTEGER, 
    date_created TEXT, 
    date_fulfilled TEXT, 
    shipping_type TEXT, 
    cc_number TEXT, 
    cc_exp_date TEXT, 
    cc_holder_name TEXT, 
    cc_type TEXT, 
    status TEXT DEFAULT 'new',
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

CREATE TABLE Order_Books (
    order_id INTEGER, 
    isbn TEXT, 
    quantity INTEGER, 
    purchase_price REAL, 
    purchase_type TEXT, 
    PRIMARY KEY (order_id, isbn),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (isbn) REFERENCES Books(isbn)
);

-- --------------------------------------------------------
-- 5. SUPPORT TICKETING & AUDIT TABLES
-- --------------------------------------------------------

CREATE TABLE Trouble_Tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category TEXT, 
    date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    created_by_student_id INTEGER, 
    created_by_emp_id INTEGER, 
    title TEXT, 
    problem_description TEXT, 
    solution_description TEXT, 
    completion_date TEXT, 
    status TEXT DEFAULT 'new', 
    resolved_by_admin_id INTEGER,
    FOREIGN KEY (created_by_student_id) REFERENCES Students(student_id),
    FOREIGN KEY (created_by_emp_id) REFERENCES Employees(emp_id),
    FOREIGN KEY (resolved_by_admin_id) REFERENCES Employees(emp_id)
);

CREATE TABLE Ticket_Status_History (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    ticket_id INTEGER, 
    old_status TEXT, 
    new_status TEXT, 
    changed_by_emp_id INTEGER, 
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES Trouble_Tickets(ticket_id),
    FOREIGN KEY (changed_by_emp_id) REFERENCES Employees(emp_id)
);
