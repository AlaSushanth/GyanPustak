# 📚 GyanPustak: Textbook Rental & Purchase Platform

### About The Project
GyanPustak is a fully functional, web-based textbook marketplace designed for university students. This project was built for the Semester VI Database Systems Lab. 

Unlike traditional multi-file applications, this system utilizes a **Monolithic Architecture**. The entire frontend interface, backend business logic, and database management system are unified within a single `app.py` file using the Streamlit framework and SQLite. 

### Key Features
* **Role-Based Access Control (RBAC):** Secure, dynamic dashboards for Students, Customer Support, Administrators, and Super-Administrators.
* **E-Commerce Pipeline:** A fully functional cart and checkout system with distinct 'Rent' and 'Buy' inventory tracking.
* **Internal Ticketing System:** A closed-loop trouble ticket triage system for handling student complaints and internal reporting.
* **Dynamic Database Initialization:** The app automatically executes DDL scripts to build and populate its own 18-table relational database upon first launch.

### How to Run This Application Locally
Since this is a unified application, running it is incredibly simple. You do not need to install a separate MySQL server.

1. Ensure you have Python installed on your computer.
2. Open your terminal or command prompt and install the required libraries:
   `pip install streamlit pandas`
3. Run the application:
   `python -m streamlit run app.py`

The application will automatically build the `GyanPustak_Final_Web_V10.db` database file and launch the interface in your default web browser!
