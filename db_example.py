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
    return execute_statement(get_connection_to_database(), statement)

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
    for period in range(FIRST_PERIOD, TENTH_PERIOD + 1):
        class_id = get_class_in_period(period)
        results = get_class_grades(class_id)

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
        print(f"Period {period} Average: {average}")


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
