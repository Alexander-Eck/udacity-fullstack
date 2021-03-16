import psycopg2

conn = psycopg2.connect(dbname='example', user='demouser', password='demopwd')

cur = conn.cursor()

cur.execute('''
    DROP TABLE IF EXISTS todos;
''')

cur.execute('''
    CREATE TABLE todos(
        id SERIAL PRIMARY KEY,
        description VARCHAR NOT NULL
    );
''')

# Insert row, method 1: hard-coded
cur.execute('''
    INSERT INTO todos (description)
    VALUES ('Buy some milk');
''')

# Insert row, method 2: string interpolation with tuple
cur.execute('''
    INSERT INTO todos (description)
    VALUES (%s);
''', ('Get a few apples',))

# Insert row, method 3: string interpolation with dictionary
sql = '''
    INSERT INTO todos (description)
    VALUES (%(description)s);
'''

data = {
    'description': 'Get back to work'
}

cur.execute(sql, data)

# Commit to transaction
conn.commit()

cur.close()
conn.close()
