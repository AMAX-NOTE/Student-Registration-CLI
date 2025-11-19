import mariadb
import sys
import os
from dotenv import load_dotenv

## Reference:
## https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
load_dotenv()
    
try:
    conn = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=3306,
        database=os.getenv("DB_NAME")
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    # TODO: Handle the error appropriately, e.g., exit or retry
    sys.exit(1)
# Create a cursor object to execute SQL queries

cur = conn.cursor()
    


def student(): 
    
    student_number = None
    
    while student_number is None:
 
        try:
            query = ("SELECT * FROM STUDENT "
             "WHERE STUDENT_NUMBER = ?")
            
            student_number = int(input("Please enter student number: "))
            cur.execute(query, (student_number,))
            
            for x in cur:
                print(f"Welcome student {x[0]}! \n")
                stu = x[1] 
                break
        
            else:
                print("\nInvalid Student Number, Try Again!!")
                student_number = None

        
        except ValueError:
            print("Invalid Student Number, Try Again!")
            

    return stu

def show_section(year, semester):
    section = []
    cur.execute("SELECT * FROM Section")
    for row in cur:
        if row[3] == year and row[2] == semester:
            section.append(row)
            
    return section
    
def add_class(student_num, available_sections):
    section_id = int(input("Enter Section_Identifier: "))
    
    for i in available_sections:
        if i[0] == section_id:
            query = ("INSERT INTO grade_report (student_number, section_identifier, grade) VALUES (?,?, NULL)")
            cur.execute(query, (student_num, section_id, ))
            conn.commit()
            print("Added Class")
            break
    else: 
        print("Error: Section Identifier may be incorrect")
            
def drop_class(student_num, available_sections):
    section_id = int(input("Enter Section_Identifier: "))
    
    for i in available_sections:
        if i[0] == section_id:
            query = ("DELETE FROM grade_report WHERE student_number = ? AND section_identifier = ? ")
            cur.execute(query, (student_num, section_id, ))
            conn.commit()
            print("Dropped Class")
            break
    else: 
        print("Error")
    
def see_schedule(student_number, year, semester):
    
    cur.execute("""
    SELECT DISTINCT 
        section.course_number,
        course_name,
        instructor
    FROM 
        (section 
        JOIN grade_report 
            ON section.section_identifier = grade_report.section_identifier)
        JOIN course 
            ON section.course_number = course.course_number
    WHERE 
        grade_report.student_number = ?
        AND Grade IS NULL
        AND year = ?
        AND semester = ?
    """,
    (student_number, year, semester)
    )
    for i in cur:
        print("Your current schedule is: \n"
              f"{i[0]}, {i[1]}, Instructor: {i[2]}\n")   

# def prereqs():
#     prereq = []
#     cur.execute("""
#         SELECT DISTINCT 
#             student_number, 
#             section.Course_Number 
#         FROM 
#             (section 
#             JOIN grade_report 
#                 ON grade_report.section_identifier = section.section_identifier)
#             JOIN prerequisite 
#                 ON section.Course_number = prerequisite.prerequisite_number
#         WHERE 
#             AND grade IS NOT NULL 
#             AND grade = "A" 
#             or grade = "B" 
#             or grade = "C"
#             """
#         )
#     for x in cur:
#         print(x)
        
def main_menu():
    # Gives student number
    
    student_number= student()
    #prereqs()
    semester = None
    year = None
    cur.execute("SELECT Semester,Year FROM section")

    while semester is None:
        
        semester = str.capitalize(input("Please enter semester: ").strip())
        cur.execute("SELECT Semester,Year FROM section")
        
        for x in cur:

            if semester == x[0]:
                break
            
        else:
            print("Invalid Semester, Try Again!")
            semester = None
    
    while year is None:
        
        year = input("Please enter year: ")
        cur.execute("SELECT Semester,Year FROM section")
        
        for x in cur:

            if year == x[1]:
                break
        else:
            print("Invalid Year, Try Again!")
            year = None
    
    section = show_section(year,semester)
    
    print(
        "\nMain Menu \n"
        "(0) Show available sections \n"
        "(1) Add a class \n"
        "(2) Drop a class \n"
        "(3) See my schedule \n"
        "(4) Exit \n")
    
    menu = None

    while True:
        
        print(
            "\nMain Menu \n"
            "(0) Show available sections \n"
            "(1) Add a class \n"
            "(2) Drop a class \n"
            "(3) See my schedule \n"
            "(4) Exit \n") 
        
        if menu == "4":
            print("Goodbye!")
            break 
        
        elif menu == "0":
            headers = ["Section_identifier", "Course_Number", "Semester", "Year", "Instructor"]
            print(*headers)
            for i in section:
                print(*i)
            menu = input("\nEnter your choice: ")
            continue
        
        elif menu == "1":
            add_class(student_number, section)
            menu = input("\nEnter your choice: ")
            continue
        
        elif menu == "2":
            drop_class(student_number, section)
            menu = input("\nEnter your choice: ")
            continue
        
        elif menu == "3":
            see_schedule(student_number, year, semester)
            menu = input("\nEnter your choice: ")
            continue
        else:
            menu = input("Enter your choice: ")
            continue

    cur.close()
    conn.close()

main_menu()


