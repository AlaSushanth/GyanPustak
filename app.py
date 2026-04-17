import streamlit as st
import sqlite3
import pandas as pd
import datetime

# V10 Database ensures a perfectly clean slate with the new Buy/Rent columns
DB_NAME = "GyanPustak_Final_Web_V10.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Universities (university_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, address TEXT, rep_first_name TEXT, rep_last_name TEXT, rep_email TEXT, rep_phone TEXT);
        CREATE TABLE IF NOT EXISTS Departments (dept_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, university_id INTEGER, FOREIGN KEY (university_id) REFERENCES Universities(university_id));
        CREATE TABLE IF NOT EXISTS Students (student_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, email TEXT UNIQUE, password TEXT NOT NULL, address TEXT, phone TEXT, dob TEXT, university_id INTEGER, major TEXT, student_status TEXT, year_of_study TEXT);
        CREATE TABLE IF NOT EXISTS Employees (emp_id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, first_name TEXT, last_name TEXT, gender TEXT, password TEXT NOT NULL, salary REAL, aadhaar_number TEXT UNIQUE, email TEXT UNIQUE, address TEXT, phone TEXT);
        CREATE TABLE IF NOT EXISTS Instructors (instructor_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, university_id INTEGER, dept_id INTEGER);
        CREATE TABLE IF NOT EXISTS Courses (course_id TEXT PRIMARY KEY, course_name TEXT, dept_id INTEGER, university_id INTEGER, year INTEGER, semester TEXT);
        CREATE TABLE IF NOT EXISTS Course_Instructors (course_id TEXT, instructor_id INTEGER, PRIMARY KEY (course_id, instructor_id));
        CREATE TABLE IF NOT EXISTS Books (isbn TEXT PRIMARY KEY, title TEXT, type TEXT, price REAL, quantity INTEGER, publisher TEXT, publication_date TEXT, edition_number TEXT, language TEXT, format TEXT, category TEXT, subcategory TEXT);
        CREATE TABLE IF NOT EXISTS Book_Authors (isbn TEXT, author_name TEXT, PRIMARY KEY (isbn, author_name));
        CREATE TABLE IF NOT EXISTS Book_Keywords (isbn TEXT, keyword TEXT, PRIMARY KEY (isbn, keyword));
        CREATE TABLE IF NOT EXISTS Course_Books (course_id TEXT, isbn TEXT, req_type TEXT, PRIMARY KEY (course_id, isbn));
        CREATE TABLE IF NOT EXISTS Book_Reviews (review_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, isbn TEXT, rating INTEGER, review_text TEXT, review_date TEXT);
        CREATE TABLE IF NOT EXISTS Cart (cart_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER UNIQUE, date_created TEXT, date_last_updated TEXT);
        
        -- NEW: Added purchase_type to Cart and Orders
        CREATE TABLE IF NOT EXISTS Cart_Books (cart_id INTEGER, isbn TEXT, quantity INTEGER, purchase_type TEXT, PRIMARY KEY (cart_id, isbn));
        CREATE TABLE IF NOT EXISTS Orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, date_created TEXT, date_fulfilled TEXT, shipping_type TEXT, cc_number TEXT, cc_exp_date TEXT, cc_holder_name TEXT, cc_type TEXT, status TEXT DEFAULT 'new');
        CREATE TABLE IF NOT EXISTS Order_Books (order_id INTEGER, isbn TEXT, quantity INTEGER, purchase_price REAL, purchase_type TEXT, PRIMARY KEY (order_id, isbn));
        
        CREATE TABLE IF NOT EXISTS Trouble_Tickets (ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP, created_by_student_id INTEGER, created_by_emp_id INTEGER, title TEXT, problem_description TEXT, solution_description TEXT, completion_date TEXT, status TEXT DEFAULT 'new', resolved_by_admin_id INTEGER);
        CREATE TABLE IF NOT EXISTS Ticket_Status_History (history_id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id INTEGER, old_status TEXT, new_status TEXT, changed_by_emp_id INTEGER, change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """)
    
    cursor.execute("SELECT COUNT(*) FROM Universities")
    if cursor.fetchone()[0] == 0:
        cursor.executescript("""
            INSERT INTO Universities (name, address, rep_first_name, rep_last_name, rep_email, rep_phone)
            VALUES ('Tech University', '101 Campus Road', 'Robert', 'Oppenheimer', 'rob@tech.edu', '555-0101'),
                   ('State College', '202 College Ave', 'Marie', 'Curie', 'marie@state.edu', '555-0202'),
                   ('Global University', '303 Earth Blvd', 'Eve', 'Polastri', 'eve@global.edu', '555-0303'),
                   ('National Institute', '404 Nation Way', 'Frank', 'Castle', 'frank@national.edu', '555-0404');

            INSERT INTO Departments (name, university_id)
            VALUES ('Computer Science', 1), ('Physics', 2), ('Mathematics', 3), ('Literature', 4);

            INSERT INTO Students (first_name, last_name, email, password, address, phone, dob, university_id, major, student_status, year_of_study)
            VALUES ('John', 'Doe', 'john.doe@email.com', 'student123', 'Apt 4B, City Center', '1234567890', '2003-05-12', 1, 'Software Engineering', 'undergraduate', '3rd'),
                   ('Jane', 'Smith', 'jane.smith@email.com', 'student123', 'Dorm 2, State Campus', '0987654321', '2001-11-23', 2, 'Applied Physics', 'graduate', '1st'),
                   ('Alice', 'Wonderland', 'alice@email.com', 'student123', '789 Rabbit Hole', '1112223333', '2004-04-01', 3, 'Mathematics', 'undergraduate', '2nd'),
                   ('Bob', 'Builder', 'bob@email.com', 'student123', '101 Construction Way', '4445556666', '2002-09-15', 4, 'Civil Engineering', 'graduate', '1st');

            INSERT INTO Employees (role, first_name, last_name, gender, password, salary, aadhaar_number, email, address, phone)
            VALUES ('Super Administrator', 'Alan', 'Turing', 'Male', 'super123', 120000.00, '[Redacted]1', 'alan.super@gyan.com', 'HQ Building', '555-9999'),
                   ('Administrator', 'Grace', 'Hopper', 'Female', 'admin123', 90000.00, '[Redacted]2', 'grace.admin@gyan.com', 'Admin Block', '555-7777'),
                   ('Customer Support', 'Ada', 'Lovelace', 'Female', 'support123', 65000.00, '[Redacted]3', 'ada.support@gyan.com', 'Support Center', '555-8888'),
                   ('Administrator', 'Charlie', 'Chaplin', 'Male', 'admin123', 85000.00, '[Redacted]4', 'charlie.admin@gyan.com', 'Comedy St', '555-4444'),
                   ('Customer Support', 'Diana', 'Prince', 'Female', 'support123', 68000.00, '[Redacted]5', 'diana.support@gyan.com', 'Themyscira', '555-5555');

            INSERT INTO Instructors (first_name, last_name, university_id, dept_id)
            VALUES ('Dr. Grace', 'Hopper', 1, 1), ('Dr. Richard', 'Feynman', 2, 2), ('Dr. Isaac', 'Newton', 3, 3), ('Dr. Mark', 'Twain', 4, 4);

            INSERT INTO Courses (course_id, course_name, dept_id, university_id, year, semester)
            VALUES ('CS101', 'Intro to Databases', 1, 1, 2026, 'Fall'), ('PHY201', 'Quantum Mechanics', 2, 2, 2026, 'Spring'),
                   ('MAT301', 'Calculus III', 3, 3, 2026, 'Fall'), ('LIT101', 'Classic Literature', 4, 4, 2026, 'Spring');

            INSERT INTO Course_Instructors (course_id, instructor_id)
            VALUES ('CS101', 1), ('PHY201', 2), ('MAT301', 3), ('LIT101', 4);

            INSERT INTO Books (isbn, title, type, price, quantity, publisher, publication_date, edition_number, language, format, category, subcategory)
            VALUES ('978-013', 'Database System Concepts', 'new', 1500.00, 50, 'McGraw Hill', '2020-03-01', '7th', 'English', 'hardcover', 'Computer Science', 'Databases'),
                   ('978-045', 'Feynman Lectures on Physics', 'used', 450.00, 20, 'Basic Books', '2011-10-04', 'New', 'English', 'softcover', 'Science', 'Physics'),
                   ('978-099', 'Calculus Early Transcendentals', 'new', 2000.00, 40, 'Cengage', '2021-01-01', '9th', 'English', 'hardcover', 'Mathematics', 'Calculus'),
                   ('978-111', 'Adventures of Huckleberry Finn', 'used', 300.00, 15, 'Penguin', '2010-05-05', 'Reprint', 'English', 'softcover', 'Literature', 'Fiction');

            INSERT INTO Book_Authors (isbn, author_name) 
            VALUES ('978-013', 'Abraham Silberschatz'), ('978-045', 'Richard P. Feynman'), ('978-099', 'James Stewart'), ('978-111', 'Mark Twain');
                   
            INSERT INTO Book_Keywords (isbn, keyword) 
            VALUES ('978-013', 'SQL'), ('978-045', 'Mechanics'), ('978-099', 'Math'), ('978-111', 'Novel');
                   
            INSERT INTO Course_Books (course_id, isbn, req_type) 
            VALUES ('CS101', '978-013', 'required'), ('PHY201', '978-045', 'recommended'), ('MAT301', '978-099', 'required'), ('LIT101', '978-111', 'recommended');

            INSERT INTO Book_Reviews (student_id, isbn, rating, review_text, review_date)
            VALUES (1, '978-013', 5, 'Heavy but very detailed.', '2026-04-01 14:00:00'),
                   (2, '978-045', 4, 'Great concepts, hard math.', '2026-04-05 09:30:00');

            INSERT INTO Cart (student_id, date_created, date_last_updated) 
            VALUES (1, '2026-04-12 10:00:00', '2026-04-12 10:05:00'), (2, '2026-04-12 11:00:00', '2026-04-12 11:05:00'),
                   (3, '2026-04-12 12:00:00', '2026-04-12 12:05:00'), (4, '2026-04-12 13:00:00', '2026-04-12 13:05:00');
                   
            INSERT INTO Cart_Books (cart_id, isbn, quantity, purchase_type) 
            VALUES (1, '978-013', 1, 'Buy'), (2, '978-045', 2, 'Rent'), (3, '978-099', 1, 'Buy'), (4, '978-111', 2, 'Rent');

            INSERT INTO Orders (student_id, date_created, date_fulfilled, shipping_type, cc_number, cc_exp_date, cc_holder_name, cc_type, status)
            VALUES (1, '2026-04-10 09:00:00', '2026-04-11 14:00:00', '2-day', '1111222233334444', '12/28', 'John Doe', 'Visa', 'shipped'),
                   (2, '2026-04-11 15:30:00', NULL, 'standard', '5555666677778888', '11/27', 'Jane Smith', 'MasterCard', 'processed'),
                   (3, '2026-04-09 10:00:00', '2026-04-10 14:00:00', '1-day', '4444555566667777', '09/29', 'Alice Wonderland', 'Visa', 'shipped'),
                   (4, '2026-04-08 11:00:00', NULL, 'standard', '8888999900001111', '05/25', 'Bob Builder', 'Amex', 'new');
                   
            INSERT INTO Order_Books (order_id, isbn, quantity, purchase_price, purchase_type) 
            VALUES (1, '978-013', 1, 1500.00, 'Buy'), (2, '978-045', 1, 450.00, 'Rent'), (3, '978-099', 1, 2000.00, 'Buy'), (4, '978-111', 1, 300.00, 'Rent');

            INSERT INTO Trouble_Tickets (category, date_logged, created_by_student_id, created_by_emp_id, title, problem_description, solution_description, completion_date, status, resolved_by_admin_id)
            VALUES ('cart', '2026-04-12 08:00:00', 1, NULL, 'Cannot add second book', 'The cart throws an error when adding book 2', NULL, NULL, 'new', NULL),
                   ('orders', '2026-04-11 10:00:00', 2, NULL, 'Tracking number missing', 'My order says shipped but no tracking', 'Emailed tracking number', '2026-04-12 09:00:00', 'completed', 1),
                   ('user profile', '2026-04-12 09:00:00', 3, NULL, 'Cannot update address', 'Address field is locked', NULL, NULL, 'assigned', NULL),
                   ('products', '2026-04-12 10:00:00', NULL, 3, 'Book image missing', 'Huckleberry Finn book has no cover image', 'Re-uploaded image', '2026-04-12 11:00:00', 'completed', 2);
        """)
    conn.commit()
    conn.close()

initialize_database()

# ==========================================
# SESSION STATE & AUTHENTICATION
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.user_id = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.user_id = None
    st.rerun()

st.set_page_config(page_title="GyanPustak Portal", layout="wide", page_icon="📚")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# BEAUTIFIED LOGIN & REGISTRATION PAGE
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📚 GyanPustak Master Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: gray; margin-bottom: 40px;'>Empowering Education Through Accessible Resources</p>", unsafe_allow_html=True)
    
    col_image, col_login = st.columns([1.2, 1], gap="large")
    
    with col_image:
        st.image("https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1000&auto=format&fit=crop", use_container_width=True)

    with col_login:
        tab_login, tab_register = st.tabs(["🔒 Secure Sign-In", "📝 New Student Sign-Up"])
        
        with tab_login:
            st.markdown("### Welcome Back")
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("Sign In 🔑", use_container_width=True)
                
                if submit:
                    conn = get_connection()
                    emp = conn.execute("SELECT * FROM Employees WHERE email = ? AND password = ?", (email, password)).fetchone()
                    if emp:
                        st.session_state.logged_in = True
                        st.session_state.user, st.session_state.role, st.session_state.user_id = emp['first_name'], emp['role'], emp['emp_id']
                        st.rerun()
                    else:
                        student = conn.execute("SELECT * FROM Students WHERE email = ? AND password = ?", (email, password)).fetchone()
                        if student:
                            st.session_state.logged_in = True
                            st.session_state.user, st.session_state.role, st.session_state.user_id = student['first_name'], 'Student', student['student_id']
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password.")
                    conn.close()
            
            st.write("---")
            st.markdown("##### 🧪 Test Credentials Quick Guide")
            st.info("""
            * **Student:** `john.doe@email.com` | Pass: `student123`
            * **Support:** `ada.support@gyan.com` | Pass: `support123`
            * **Admin:** `grace.admin@gyan.com` | Pass: `admin123`
            * **Super Admin:** `alan.super@gyan.com` | Pass: `super123`
            """)

        with tab_register:
            st.markdown("### Create a Student Account")
            with st.form("register_form", clear_on_submit=True):
                r_first = st.text_input("First Name*")
                r_last = st.text_input("Last Name*")
                r_email = st.text_input("Email Address*")
                r_pass = st.text_input("Create Password*", type="password")
                
                st.write("**Academic Details**")
                col1, col2 = st.columns(2)
                r_uni = col1.number_input("University ID* (e.g. 1 or 2)", min_value=1, step=1)
                r_major = col2.text_input("Major Field of Study")
                r_status = col1.selectbox("Student Status", ["undergraduate", "graduate"])
                r_year = col2.selectbox("Year of Study", ["1st", "2nd", "3rd", "4th", "5th+"])
                
                st.write("**Contact Details**")
                r_phone = st.text_input("Phone Number")
                r_address = st.text_area("Home/Dorm Address")
                
                min_date = datetime.date(1950, 1, 1)
                max_date = datetime.date.today()
                default_date = datetime.date(2005, 1, 1)
                r_dob = st.date_input("Date of Birth", value=default_date, min_value=min_date, max_value=max_date)
                
                reg_submit = st.form_submit_button("Create Account 🚀", use_container_width=True)
                
                if reg_submit:
                    if not r_first or not r_last or not r_email or not r_pass:
                        st.error("Please fill in all required fields marked with an asterisk (*).")
                    else:
                        try:
                            conn = get_connection()
                            conn.execute("""
                                INSERT INTO Students 
                                (first_name, last_name, email, password, address, phone, dob, university_id, major, student_status, year_of_study) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (r_first, r_last, r_email, r_pass, r_address, r_phone, str(r_dob), r_uni, r_major, r_status, r_year))
                            conn.commit()
                            conn.close()
                            st.success("✅ Account created successfully! Please switch to the Sign-In tab to log in.")
                        except sqlite3.IntegrityError:
                            st.error("❌ An account with this email address already exists.")

# ==========================================
# MAIN DASHBOARDS
# ==========================================
else:
    st.sidebar.title(f"Welcome, {st.session_state.user}")
    st.sidebar.write(f"**Role:** {st.session_state.role}")
    st.sidebar.button("Logout", on_click=logout, use_container_width=True)
    st.sidebar.divider()

    # ----------------------------------------
    # 1. STUDENT DASHBOARD
    # ----------------------------------------
    if st.session_state.role == 'Student':
        st.title("🎓 Student Dashboard")
        menu = st.sidebar.radio("Navigation", ["Browse Books", "My Cart", "Checkout & Orders", "My Reviews", "Support Tickets"])
        
        if menu == "Browse Books":
            st.subheader("📚 Book Inventory")
            conn = get_connection()
            # Pulled basic details for display
            df = pd.read_sql_query("SELECT isbn, title, type as 'Condition', price, quantity as 'Stock' FROM Books", conn)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("### 🛒 Add to Your Cart")
            with st.form("add_cart"):
                # New Interactive Dropdown for Book Selection
                book_options = [f"{row['isbn']} - {row['title']} (₹{row['price']})" for _, row in df.iterrows()]
                selected_book = st.selectbox("1. Select a Book from the Library:", book_options)
                
                colA, colB = st.columns(2)
                # New Interactive Buy/Rent radio selector
                purchase_type = colA.radio("2. Transaction Type:", ["Buy", "Rent"], horizontal=True)
                qty = colB.number_input("3. Quantity:", min_value=1, step=1)
                
                if st.form_submit_button("Add to Cart") and selected_book:
                    isbn_extracted = selected_book.split(" - ")[0]
                    
                    cart = conn.execute("SELECT cart_id FROM Cart WHERE student_id = ?", (st.session_state.user_id,)).fetchone()
                    cart_id = cart[0] if cart else conn.execute("INSERT INTO Cart (student_id) VALUES (?)", (st.session_state.user_id,)).lastrowid
                    
                    # Inserting choice into the database
                    conn.execute("INSERT OR REPLACE INTO Cart_Books (cart_id, isbn, quantity, purchase_type) VALUES (?, ?, ?, ?)", 
                                 (cart_id, isbn_extracted, qty, purchase_type))
                    conn.commit()
                    st.success(f"Success! Added {qty}x '{purchase_type}' option for {isbn_extracted} to your cart.")
            conn.close()
            
        elif menu == "My Cart":
            st.subheader("🛒 My Cart")
            conn = get_connection()
            # Updated query to pull the user's specific Buy/Rent choice
            df = pd.read_sql_query("SELECT CB.isbn, B.title, CB.purchase_type as 'Rent / Buy', B.price, CB.quantity FROM Cart C JOIN Cart_Books CB ON C.cart_id = CB.cart_id JOIN Books B ON CB.isbn = B.isbn WHERE C.student_id = ?", conn, params=(st.session_state.user_id,))
            if df.empty: st.warning("Cart is empty.")
            else:
                st.dataframe(df, use_container_width=True)
                st.info(f"**Total: ₹{(df['price'] * df['quantity']).sum()}**")
                with st.form("remove_cart"):
                    rem_isbn = st.text_input("Enter ISBN to remove:")
                    if st.form_submit_button("Remove Book"):
                        cart_id = conn.execute("SELECT cart_id FROM Cart WHERE student_id = ?", (st.session_state.user_id,)).fetchone()[0]
                        conn.execute("DELETE FROM Cart_Books WHERE cart_id = ? AND isbn = ?", (cart_id, rem_isbn))
                        conn.commit()
                        st.success("Removed from cart.")
                        st.rerun()
            conn.close()
            
        elif menu == "Checkout & Orders":
            tab1, tab2 = st.tabs(["Checkout Cart", "My Order History"])
            with tab1:
                st.subheader("Secure Checkout")
                conn = get_connection()
                cart = conn.execute("SELECT cart_id FROM Cart WHERE student_id = ?", (st.session_state.user_id,)).fetchone()
                
                if not cart or not conn.execute("SELECT 1 FROM Cart_Books WHERE cart_id=?", (cart[0],)).fetchone():
                    st.warning("Your cart is empty. Nothing to checkout.")
                else:
                    with st.form("checkout_form"):
                        ship_type = st.selectbox("Shipping Type", ["Standard (Free)", "2-Day (₹150)", "1-Day Express (₹300)"])
                        pay_method = st.selectbox("Payment Method", ["Credit/Debit Card", "Online Pay (UPI)", "Cash on Delivery"])
                        st.write("---")
                        st.write("**Payment Details** (Required for Card)")
                        colA, colB = st.columns(2)
                        cc_type = colA.selectbox("Card Type", ["Visa", "MasterCard", "Amex", "N/A (Non-Card)"])
                        cc_num = colB.text_input("Card Number (16 Digits)")
                        cc_exp = colA.text_input("Expiry Date (MM/YY)")
                        cc_name = colB.text_input("Cardholder Name")
                        
                        if st.form_submit_button("Confirm Order & Pay"):
                            final_cc = cc_num if pay_method == "Credit/Debit Card" else "N/A"
                            final_exp = cc_exp if pay_method == "Credit/Debit Card" else "N/A"
                            final_name = cc_name if pay_method == "Credit/Debit Card" else "N/A"
                            final_type = cc_type if pay_method == "Credit/Debit Card" else pay_method
                            
                            stype_doc = "standard" if "Standard" in ship_type else "2-day" if "2-Day" in ship_type else "1-day"
                            
                            conn.execute("INSERT INTO Orders (student_id, shipping_type, cc_type, cc_number, cc_exp_date, cc_holder_name, status) VALUES (?, ?, ?, ?, ?, ?, 'new')", 
                                         (st.session_state.user_id, stype_doc, final_type, final_cc, final_exp, final_name))
                            order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
                            
                            items = conn.execute("SELECT CB.isbn, CB.quantity, CB.purchase_type, B.price FROM Cart_Books CB JOIN Books B ON CB.isbn = B.isbn WHERE CB.cart_id = ?", (cart[0],)).fetchall()
                            for item in items:
                                conn.execute("INSERT INTO Order_Books (order_id, isbn, quantity, purchase_price, purchase_type) VALUES (?, ?, ?, ?, ?)", 
                                             (order_id, item['isbn'], item['quantity'], item['price'], item['purchase_type']))
                                conn.execute("UPDATE Books SET quantity = quantity - ? WHERE isbn = ?", (item['quantity'], item['isbn']))
                            conn.execute("DELETE FROM Cart_Books WHERE cart_id = ?", (cart[0],))
                            conn.commit()
                            st.success(f"Payment Successful! Order #{order_id} placed.")
                conn.close()
            with tab2:
                conn = get_connection()
                # Updated Order History Query to show Rent/Buy properly
                df = pd.read_sql_query("SELECT O.order_id, O.status, O.shipping_type, B.title, OB.purchase_type as 'Rent / Buy', OB.quantity, OB.purchase_price FROM Orders O JOIN Order_Books OB ON O.order_id = OB.order_id JOIN Books B ON OB.isbn = B.isbn WHERE O.student_id = ?", conn, params=(st.session_state.user_id,))
                st.dataframe(df.fillna('N/A'), use_container_width=True)
                conn.close()
                
        elif menu == "My Reviews":
            st.title("⭐ My Book Reviews")
            tab1, tab2 = st.tabs(["Write a Review", "View My Submitted Reviews"])
            with tab1:
                with st.form("review_form"):
                    isbn = st.text_input("Book ISBN to review:")
                    rating = st.slider("Rating (1-5)", 1, 5, 5)
                    text = st.text_area("Write your review here:")
                    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if st.form_submit_button("Submit Review"):
                        conn = get_connection()
                        conn.execute("INSERT INTO Book_Reviews (student_id, isbn, rating, review_text, review_date) VALUES (?, ?, ?, ?, ?)", (st.session_state.user_id, isbn, rating, text, date_now))
                        conn.commit()
                        conn.close()
                        st.success("Thank you! Your review has been successfully submitted.")
            with tab2:
                conn = get_connection()
                df = pd.read_sql_query("""SELECT B.title as "Book Title", R.rating as "Stars", R.review_text as "Review", R.review_date as "Date" FROM Book_Reviews R JOIN Books B ON R.isbn = B.isbn WHERE R.student_id = ?""", conn, params=(st.session_state.user_id,))
                if df.empty: st.info("You haven't submitted any reviews yet.")
                else: st.dataframe(df.fillna('N/A'), use_container_width=True)
                conn.close()
                
        elif menu == "Support Tickets":
            tab1, tab2 = st.tabs(["Open a New Ticket", "My Ticket History"])
            with tab1:
                st.info("Per policy, tickets submitted by students begin as 'new' and are initially handled by Customer Support.")
                with st.form("ticket_form"):
                    cat = st.selectbox("Category", ["user profile", "products", "cart", "orders", "other"])
                    title = st.text_input("Issue Title")
                    desc = st.text_area("Description")
                    if st.form_submit_button("Open Ticket"):
                        conn = get_connection()
                        conn.execute("INSERT INTO Trouble_Tickets (category, created_by_student_id, title, problem_description, status) VALUES (?, ?, ?, ?, 'new')", (cat, st.session_state.user_id, title, desc))
                        conn.commit()
                        conn.close()
                        st.success("Ticket opened successfully!")
                        
            with tab2:
                st.subheader("My Submitted Tickets")
                conn = get_connection()
                df = pd.read_sql_query("""
                    SELECT ticket_id, status, category, title, problem_description, solution_description as 'Admin Solution', completion_date 
                    FROM Trouble_Tickets 
                    WHERE created_by_student_id = ?
                """, conn, params=(st.session_state.user_id,))
                if df.empty:
                    st.info("You have not submitted any support tickets yet.")
                else:
                    st.dataframe(df.fillna('Pending'), use_container_width=True)
                conn.close()

    # ----------------------------------------
    # 2. CUSTOMER SUPPORT DASHBOARD
    # ----------------------------------------
    elif st.session_state.role == 'Customer Support':
        st.title("🎧 Support Dashboard")
        menu = st.sidebar.radio("Navigation", ["Manage Tickets", "Cancel Orders", "Report Internal Issue"])
        
        conn = get_connection()
        if menu == "Manage Tickets":
            st.write("---")
            st.write("**All Tickets View**")
            df = pd.read_sql_query("SELECT ticket_id, status, category, title, problem_description, created_by_student_id as student_creator FROM Trouble_Tickets", conn)
            st.dataframe(df.fillna('N/A'), use_container_width=True)
            
            st.write("---")
            st.write("**Assign 'New' Tickets to Administrators**")
            with st.form("assign_ticket"):
                t_id = st.number_input("Ticket ID to Process", min_value=1, step=1)
                if st.form_submit_button("Assign to Administrator"):
                    ticket = conn.execute("SELECT status FROM Trouble_Tickets WHERE ticket_id=?", (t_id,)).fetchone()
                    if ticket and ticket['status'] == 'new':
                        conn.execute("UPDATE Trouble_Tickets SET status='assigned' WHERE ticket_id=?", (t_id,))
                        conn.execute("INSERT INTO Ticket_Status_History (ticket_id, old_status, new_status, changed_by_emp_id) VALUES (?, 'new', 'assigned', ?)", (t_id, st.session_state.user_id))
                        conn.commit()
                        st.success(f"Ticket #{t_id} assigned to Administrators.")
                        st.rerun()  # <--- THIS IS THE FIX THAT REFRESHES THE TABLE INSTANTLY
                    else:
                        st.error("You can only modify tickets that currently have a 'new' status.")
                        
        elif menu == "Cancel Orders":
            st.write("---")
            st.write("**Active Orders**")
            df_ord = pd.read_sql_query("SELECT order_id, student_id, status, date_created FROM Orders WHERE status != 'canceled'", conn)
            st.dataframe(df_ord.fillna('N/A'), use_container_width=True)
            with st.form("cancel_form"):
                o_id = st.number_input("Order ID to Cancel", min_value=1, step=1)
                if st.form_submit_button("Process Cancellation"):
                    conn.execute("UPDATE Orders SET status='canceled' WHERE order_id=?", (o_id,))
                    conn.commit()
                    st.success(f"Order #{o_id} has been canceled per support procedure.")
                    
        elif menu == "Report Internal Issue":
            with st.form("emp_ticket"):
                cat = st.selectbox("Category", ["user profile", "products", "cart", "orders", "other"])
                title = st.text_input("Issue Title")
                desc = st.text_area("Description")
                if st.form_submit_button("Submit Internal Ticket"):
                    conn.execute("INSERT INTO Trouble_Tickets (category, created_by_emp_id, title, problem_description, status) VALUES (?, ?, ?, ?, 'assigned')", (cat, st.session_state.user_id, title, desc))
                    conn.commit()
                    st.success("Internal ticket submitted to Administrators.")
        conn.close()

    # ----------------------------------------
    # 3. ADMIN DASHBOARD
    # ----------------------------------------
    elif st.session_state.role == 'Administrator':
        st.title("⚙️ Admin Dashboard")
        menu = st.sidebar.radio("Navigation", ["Resolve Tickets", "Manage Shipping", "Manage Inventory"])
        
        conn = get_connection()
        if menu == "Resolve Tickets":
            df = pd.read_sql_query("SELECT ticket_id, status, category, title, problem_description FROM Trouble_Tickets WHERE status IN ('assigned', 'in-process', 'completed')", conn)
            st.dataframe(df.fillna('N/A'), use_container_width=True)
            
            with st.form("admin_ticket"):
                t_id = st.number_input("Ticket ID", min_value=1, step=1)
                new_status = st.selectbox("Update Status To", ["in-process", "completed"])
                sol = st.text_area("Solution Description (If completed)")
                c_date = datetime.datetime.now().strftime("%Y-%m-%d") if new_status == 'completed' else "N/A"
                if st.form_submit_button("Apply Resolution"):
                    ticket = conn.execute("SELECT status FROM Trouble_Tickets WHERE ticket_id=?", (t_id,)).fetchone()
                    if ticket and ticket['status'] in ['assigned', 'in-process']:
                        conn.execute("UPDATE Trouble_Tickets SET status=?, solution_description=?, completion_date=?, resolved_by_admin_id=? WHERE ticket_id=?", (new_status, sol, c_date, st.session_state.user_id, t_id))
                        conn.execute("INSERT INTO Ticket_Status_History (ticket_id, old_status, new_status, changed_by_emp_id) VALUES (?, ?, ?, ?)", (t_id, ticket['status'], new_status, st.session_state.user_id))
                        conn.commit()
                        st.success(f"Ticket #{t_id} resolved/updated successfully.")
                        st.rerun() # Refresh Table Here Too
                    else:
                        st.error("Invalid ticket ID or ticket is not available for Admin resolution.")
                        
        elif menu == "Manage Shipping":
            df = pd.read_sql_query("SELECT * FROM Orders", conn)
            st.dataframe(df.fillna('N/A'), use_container_width=True)
            with st.form("update_order"):
                o_id = st.number_input("Order ID", min_value=1, step=1)
                new_status = st.selectbox("Status", ["processed", "awaiting shipping", "shipped"])
                f_date = datetime.datetime.now().strftime("%Y-%m-%d") if new_status == 'shipped' else "N/A"
                if st.form_submit_button("Update Shipping Workflow"):
                    conn.execute("UPDATE Orders SET status=?, date_fulfilled=? WHERE order_id=?", (new_status, f_date, o_id))
                    conn.commit()
                    st.success(f"Order #{o_id} advanced to {new_status}.")
                    st.rerun() # Refresh Table Here Too
                    
        elif menu == "Manage Inventory":
            with st.form("book_form"):
                isbn, title = st.text_input("ISBN"), st.text_input("Title")
                b_type = st.selectbox("Type", ["new", "used"])
                price, qty = st.number_input("Price"), st.number_input("Qty", step=1)
                if st.form_submit_button("Add Book to Database"):
                    conn.execute("INSERT INTO Books (isbn, title, type, price, quantity) VALUES (?, ?, ?, ?, ?)", (isbn, title, b_type, price, qty))
                    conn.commit()
                    st.success("Book Added!")
        conn.close()

    # ----------------------------------------
    # 4. SUPER ADMIN DASHBOARD
    # ----------------------------------------
    elif st.session_state.role == 'Super Administrator':
        st.title("👑 Super Admin Dashboard")
        menu = st.sidebar.radio("Navigation", [
            "Register Staff", 
            "View Employees", 
            "Organization Setup", 
            "Database Explorer", 
            "Delete Records"
        ])
        
        conn = get_connection()
        
        if menu == "Register Staff":
            st.info("The Super Administrator has authority to add new customer support and administrator employees.")
            with st.form("reg_user"):
                role = st.selectbox("Assign Employee Role", ["Administrator", "Customer Support"])
                fname, lname = st.text_input("First Name"), st.text_input("Last Name")
                email, pwd = st.text_input("Email"), st.text_input("Temporary Password", type="password")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                salary = st.number_input("Salary", min_value=0.0)
                aadhaar = st.text_input("Aadhaar Number")
                address, phone = st.text_input("Address"), st.text_input("Phone Number")
                
                if st.form_submit_button("Register Employee"):
                    try:
                        conn.execute("INSERT INTO Employees (role, first_name, last_name, gender, email, password, salary, aadhaar_number, address, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                     (role, fname, lname, gender, email, pwd, salary, aadhaar, address, phone))
                        conn.commit()
                        st.success(f"New {role} registered successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
        elif menu == "View Employees":
            st.subheader("👥 Employee Roster")
            df = pd.read_sql_query("SELECT emp_id, role, first_name, last_name, email, gender, salary, phone FROM Employees", conn)
            st.dataframe(df.fillna('N/A'), use_container_width=True)

        elif menu == "Organization Setup":
            st.subheader("🏢 Organization Setup")
            tab1, tab2, tab3 = st.tabs(["Add University", "Add Department", "Add Course"])
            
            with tab1:
                with st.form("uni_form"):
                    u_name, u_addr = st.text_input("University Name"), st.text_input("Address")
                    rep_fn, rep_ln = st.text_input("Rep First Name"), st.text_input("Rep Last Name")
                    rep_email, rep_phone = st.text_input("Rep Email"), st.text_input("Rep Phone")
                    if st.form_submit_button("Add University"):
                        conn.execute("INSERT INTO Universities (name, address, rep_first_name, rep_last_name, rep_email, rep_phone) VALUES (?, ?, ?, ?, ?, ?)", (u_name, u_addr, rep_fn, rep_ln, rep_email, rep_phone))
                        conn.commit()
                        st.success("University added!")
                        
            with tab2:
                with st.form("dept_form"):
                    d_name = st.text_input("Department Name")
                    uni_df = pd.read_sql_query("SELECT university_id, name FROM Universities", conn)
                    uni_dict = dict(zip(uni_df.name, uni_df.university_id)) if not uni_df.empty else {}
                    sel_uni = st.selectbox("Select University", list(uni_dict.keys()) if uni_dict else ["No Universities Available"])
                    
                    if st.form_submit_button("Add Department") and uni_dict:
                        conn.execute("INSERT INTO Departments (name, university_id) VALUES (?, ?)", (d_name, uni_dict[sel_uni]))
                        conn.commit()
                        st.success("Department added!")
                            
            with tab3:
                with st.form("course_form"):
                    c_id, c_name = st.text_input("Course ID (e.g., CS101)"), st.text_input("Course Name")
                    c_year, c_sem = st.number_input("Year", value=2026), st.selectbox("Semester", ["Fall", "Spring", "Summer"])
                    
                    uni_df = pd.read_sql_query("SELECT university_id, name FROM Universities", conn)
                    uni_dict = dict(zip(uni_df.name, uni_df.university_id)) if not uni_df.empty else {}
                    sel_uni = st.selectbox("Select University for Course", list(uni_dict.keys()) if uni_dict else ["None"])
                    
                    dept_df = pd.read_sql_query("SELECT dept_id, name FROM Departments", conn)
                    dept_dict = dict(zip(dept_df.name, dept_df.dept_id)) if not dept_df.empty else {}
                    sel_dept = st.selectbox("Select Department", list(dept_dict.keys()) if dept_dict else ["None"])
                    
                    if st.form_submit_button("Add Course") and uni_dict and dept_dict:
                        conn.execute("INSERT INTO Courses (course_id, course_name, dept_id, university_id, year, semester) VALUES (?, ?, ?, ?, ?, ?)", (c_id, c_name, dept_dict[sel_dept], uni_dict[sel_uni], c_year, c_sem))
                        conn.commit()
                        st.success("Course added!")
                        
        elif menu == "Database Explorer":
            st.markdown("### 🔍 Global Database Explorer")
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'", conn)
            selected_table = st.selectbox("Select a table to view", tables['name'].tolist())
            if selected_table:
                df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
                df_clean = df.fillna("N/A")
                st.dataframe(df_clean, use_container_width=True)
                
        elif menu == "Delete Records":
            st.warning("⚠️ WARNING: This permanently deletes data.")
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'", conn)
            selected_table = st.selectbox("Select Table", tables['name'].tolist())
            if selected_table:
                cols = pd.read_sql_query(f"PRAGMA table_info({selected_table})", conn)['name'].tolist()
                with st.form("del_form"):
                    col_name = st.selectbox("Filter by Column", cols)
                    val = st.text_input("Exact Value to Delete")
                    if st.form_submit_button("PERMANENTLY DELETE"):
                        conn.execute(f"DELETE FROM {selected_table} WHERE {col_name} = ?", (val,))
                        conn.commit()
                        st.success("Record deleted.")
        conn.close()