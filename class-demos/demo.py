import psycopg2

connection = psycopg2.connect('dbname=postgres user=Yousif password=yousif')
cursor = connection.cursor()

cursor.execute('''insert into students 
                    (id, name, age)
                    values (%s, %s, %s);''', (4, 'rana', 23))

SQL = 'insert into students (id, name, age) values (%(id)s, %(name)s, %(age)s)'
data = {'id': 5,
        'name': 'mahmoud',
        'age': 20}
cursor.execute(SQL, data)

cursor.execute('select * from students;')
print(cursor.fetchall())

connection.commit()
cursor.close()
connection.close()