import re

import mysql.connector

FIRST_PERIOD = 1
TENTH_PERIOD = 10


def get_connection_to_database():
    return mysql.connector.connect(user='munima',
                                   password='233179548',
                                   host='10.8.37.226',
                                   database='munima_db')


def execute_statement(connection, statement):
    cursor = connection.cursor()
    cursor.execute(statement)

    results = []
    for row in cursor:
        results.append(row)

    cursor.close()
    connection.commit()
    connection.close()
    return results


def get_student_schedule():
    statement = f"CALL Get_Student_Schedule({student_id})"
    return execute_statement(get_connection_to_database(), statement)


def get_class_grades(class_id):
    statement = f"CALL Get_Grades_For_Class({student_id}, {class_id})"
    return execute_statement(get_connection_to_database(), statement)


def get_class_in_period(period):
    statement = f"SELECT pd{period} FROM Schedules WHERE scheduleID={student_id}"
    return execute_statement(get_connection_to_database(), statement)[0][0]


def get_class_name(class_id):
    statement = f"SELECT courseName FROM CourseOfferings INNER JOIN Courses ON Courses.courseID = CourseOfferings.course WHERE offeringID = {class_id};"
    return execute_statement(get_connection_to_database(), statement)[0][0]


def get_teacher_schedule():
    statement = f"SELECT * FROM CourseOfferings WHERE Teacher={teacher_id}"
    return execute_statement(get_connection_to_database(), statement)

def get_assignment_list(class_period_selected):
    for offering in get_teacher_schedule():
        if offering[4] == class_period_selected:
            statement = f"SELECT assignmentID, assignment FROM CoursesWork WHERE offeringID={offering[0]}"
            return execute_statement(get_connection_to_database(), statement)
    return "error"


def view_student_schedule():
    results = get_student_schedule()
    print(results)

    for row in results:
        period = row[0]
        course = row[1]
        room = row[2]
        teacher = row[3]
        print(f"Period: {period}")
        print(f"Course: {course}")
        print(f"Room: {room}")
        print(f"Teacher: {teacher}")
        print()


def view_class_specific_grades(class_id):
    results = get_class_grades(class_id)

    for row in results:
        print(f"Assignment: {row[0]}  Grade: {row[1]}")


def view_overall_grades():
    ap_grade_added = 0
    ap_amt = 0
    regular_grade_added = 0
    regular_amt = 0
    for period in range(FIRST_PERIOD, TENTH_PERIOD + 1):
        class_id = get_class_in_period(period)
        results = get_class_grades(class_id)
        class_name = get_class_name(get_class_in_period(period))

        minor_grades = 0
        minor_grade_amt = 0
        major_grades = 0
        major_grade_amt = 0

        for assignment in results:
            if assignment[0] == 'Homework':
                minor_grades += assignment[1]
                minor_grade_amt += 1
            else:
                major_grades += assignment[1]
                major_grade_amt += 1

        major_grades /= major_grade_amt
        minor_grades /= minor_grade_amt

        average = ((major_grades * 0.7) + (minor_grades * 0.3))
        average *= 100

        newavg = int(average)
        newavg /= 100

        stringavg = str(newavg)
        extrazero = ""

        if len(stringavg) == 4:
            extrazero = "0"

        if re.search("AP", class_name) != None:
            ap_grade_added += newavg
            ap_amt += 1
        else:
            regular_grade_added += newavg
            regular_amt += 1
        print(f"{class_name} Average: {newavg}{extrazero}%")

    ap_avg = 0
    if ap_amt > 0:
        ap_avg = ap_grade_added / ap_amt

    regular_avg = regular_grade_added / regular_amt

    total_avg = (ap_avg * 1.1 + regular_avg) / 2

    print(f"Total Average: {total_avg}")

def view_teacher_schedule():
    busy_periods = get_teacher_schedule()
    for i in range(FIRST_PERIOD, TENTH_PERIOD + 1):
        busy = False
        for offering in busy_periods:
            if offering[4] == i:
                busy = True
                print(f"{i}: {get_class_name(offering[0])}")
                break
        if not busy:
            print(f"{i}: Free")

print("Welcome are you a:\n1. Student\n2. Teacher\n3. Administrator")

user_type = input("Choice: ")
user_type = int(user_type)

if user_type == 1:

    student_id = input("Enter StudentID: ")
    option_chosen = -1

    while int(option_chosen) != 4:
        option_chosen = input("Choose An Option\n1. Schedule\n2. Class Specific Grades\n3. Overall Grade\n4. "
                              "Quit\n\nChoice: ")
        if int(option_chosen) == 1:
            view_student_schedule()
        elif int(option_chosen) == 2:
            selected_period = input("Enter period you take this class: ")
            course_offering_id = get_class_in_period(selected_period)
            view_class_specific_grades(course_offering_id)
        elif int(option_chosen) == 3:
            view_overall_grades()
elif user_type == 2:

    teacher_id = input("Enter TeacherID: ")
    option_chosen = -1

    while option_chosen != 3:
        option_chosen = input("Choose An Option\n1. Schedule\n2. Select Class\n3. Quit\nChoice: ")
        option_chosen = int(option_chosen)

        if option_chosen == 1:
            view_teacher_schedule()
        elif option_chosen == 2:
            class_period_selected = int(input("Enter Class Period: "))
            assignment_list = get_assignment_list(class_period_selected)

            if assignment_list == "error":
                print("error, you have no class that period")
            else:
                print("ID | Type")
                for assignment in assignment_list:
                    print(f"{assignment[0]} | {assignment[1]}")