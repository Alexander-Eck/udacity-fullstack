import psycopg2

# Establish connection with DB
conn = psycopg2.connect(dbname="example", user="demouser", password="demopwd")

# Create a cursor to start interacting
cur = conn.cursor()

# Drop table if exists - start fresh
cur.execute("""
    DROP TABLE IF EXISTS todos;
""")

# Create the table 'todos'
cur.execute("""
    CREATE TABLE todos(
        id serial PRIMARY KEY,
        description VARCHAR NOT NULL
    );
""")

# Commit transaction
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
 