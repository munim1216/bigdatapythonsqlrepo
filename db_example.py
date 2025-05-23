import mysql.connector


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


def get_student_schedule(student_id):
    statement = f"CALL Get_Student_Schedule({student_id})"
    return execute_statement(get_connection_to_database(), statement)


def get_class_grades(student_id, class_id):
    statement = f"CALL Get_Grades_For_Class({student_id}, {class_id})"
    return execute_statement(get_connection_to_database(), statement)


def get_class_in_period(student_id, period):
    statement = f"SELECT pd{period} FROM Schedules WHERE scheduleID={student_id}"
    print(statement)
    return execute_statement(get_connection_to_database(), statement)


def view_student_schedule():
    results = get_student_schedule(student_id)
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
    results = get_class_grades(student_id, class_id)

    for row in results:
        print(f"Assignment: {row[0]}  Grade: {row[1]}")


student_id = input("Enter StudentID: ")
option_chosen = -1

while option_chosen != 4:
    option_chosen = input("Choose An Option\n1. Schedule\n2. Class Specific Grades\n3. Overall Grade\n4. "
                          "Quit\n\nChoice: ")
    if int(option_chosen) == 1:
        view_student_schedule()
    elif int(option_chosen) == 2:
        selected_period = input("Enter period you take this class: ")
        print(selected_period)
        course_offering_id = get_class_in_period(student_id, selected_period)[0]
        print(course_offering_id)
        #view_class_specific_grades(course_offering_id)
