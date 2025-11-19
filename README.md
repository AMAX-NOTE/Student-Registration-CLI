
# Student Registration Management System

A robust Command Line Interface (CLI) tool designed to manage university course enrollments, schedules, and student data. The application interfaces securely with a remote MariaDB instance to perform ACID-compliant transactions.

## Key Features
- **Secure Database Integration:** Utilizes the `mariadb` connector to establish authenticated sessions with remote database servers.
- **CRUD Operations:** Implements parameterized SQL queries to safely Add/Drop classes, preventing SQL injection vulnerabilities.
- **Complex Reporting:** Generates student schedules by joining `Section`, `Grade_Report`, and `Course` tables dynamically.
- **Error Handling:** Comprehensive try/except blocks manage connection timeouts, invalid user inputs (e.g., string injection in integer fields), and database exceptions.

## Technical Stack
- **Language:** Python 3.x
- **Database:** MariaDB / MySQL
- **Concepts:** SQL Joins, Parameterized Queries, Input Validation

## Usage
Ensure you have the `mariadb` connector installed:
```bash
pip install mariadb
python Registration.py
