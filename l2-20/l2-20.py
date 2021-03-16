import psycopg2

# Establish DB connection and create a cursor
conn = psycopg2.connect(dbname='example', user='demouser', password='demopwd')

cur = conn.cursor()

# Reset table
cur.execute('''
    DROP TABLE IF EXISTS todos;
''')

cur.execute('''
    CREATE TABLE todos(
        id SERIAL PRIMARY KEY,
        description VARCHAR NOT NULL
    );
''')

# Insert 3 rows of data
sql = '''
    INSERT INTO todos (description)
    VALUES (%(description)s);
'''

data = (
    {'description': 'Buy some milk'},
    {'description': 'Get a few apples'},
    {'description': 'Get back to work'}
)

for i in data:
    cur.execute(sql, i)

# Fetch a row from the table, alter the text, and create a new record
cur.execute('SELECT description FROM todos LIMIT 1;')

result = cur.fetchone()

data = {'description': result[0].replace('milk', 'water')}

cur.execute(sql, data)

# Fetch all rows from the table, print each item line-by-line
cur.execute('SELECT description FROM todos;')

result = cur.fetchall()

for r in result:
    print(r)

# Commit to transaction
conn.commit()

# Close cursor and connection
cur.close()
conn.close()