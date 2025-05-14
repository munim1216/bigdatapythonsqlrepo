import mysql.connector


def get_connection_to_database():
    return mysql.connector.connect(user='munima',
                                   password='233179548',
                                   host='10.8.37.226',
                                   database='munima_db')


connection = get_connection_to_database()
cursor = connection.cursor()

query = "SELECT * FROM Departments"

cursor.execute(query)

print("Select a department name:")

for row in cursor:
    print("" + str(row[0]) + ".", row[1])

department = input("Enter your department choice: ")

query = f"SELECT teacherName FROM Teachers WHERE department={department}"

cursor.execute(query)

for row in cursor:
    print(row[0])
cursor.close()
connection.close()
