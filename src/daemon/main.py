import psycopg2

connection = None
cursor = None

try:
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="xml",
                                  port="5432",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teachers")

    print("Teachers list:")
    for teacher in cursor:
        print(f" > {teacher[0]}, from {teacher[1]}")

except (Exception, psycopg2.Error) as error:
    print("Failed to fetch shared-data", error)

finally:
    if connection:
        cursor.close()
        connection.close()
