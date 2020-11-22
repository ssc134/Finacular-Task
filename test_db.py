import psycopg2
from datetime import datetime

connection = psycopg2.connect(
    database="test", user="saurabh", password="admin", host="127.0.0.1", port="5432"
)
print("Database successfully opened.")

cursor = connection.cursor()

"""
cursor.execute("CREATE TABLE test (id SERIAL PRIMARY KEY NOT NULL, date DATE NOT NULL, price real NOT NULL);")
print("Table successfully created.")
"""

#cursor.execute("CREATE SEQUENCE books_sequence start 1 increment 1;")
cursor.execute(
    """INSERT INTO test (id, date, price) VALUES (%s,to_date(%s, 'DD Mon YYYY'),%s);""",
    (1, "20 Nov 2020", 2006.47),
)
# (nextval('test_sequence'), {datetime.date(2005,11,18)}, 2006.47);")
print("Record successfully inserted.")

connection.commit()

cursor.execute(f"""SELECT * FROM test;""")
rows = cursor.fetchall()
for row in rows:
    print("Date = ", row[1])
    print("Price = ", row[2])
print("Operation successfully executed")


connection.close()