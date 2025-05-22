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


student_id = input("Enter StudentID: ")

results = get_student_schedule(student_id)

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

