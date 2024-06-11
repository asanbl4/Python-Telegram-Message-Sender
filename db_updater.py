import psycopg2
import pandas as pd
from datetime import datetime

df = pd.read_csv('students_to_db.csv')
table_name = 'students'

conn = psycopg2.connect(
    database='students',
    host='localhost',
    user='postgres',
    password='postgres',
    port='5432'
)
cursor = conn.cursor()

try:
    for index, row in df.iterrows():
        birthday_date = None
        if not pd.isna(row['birthday']):
            birthday_date = datetime.strptime(row['birthday'], '%d.%m.%Y').date()
        query = f"""
                INSERT INTO {table_name} 
                (id, first_name, last_name, handle, email, format, homework, birthday) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, (
            row['id'],
            row['first_name'],
            row['last_name'],
            row['handle'],
            row['email'],
            row['format'],
            row['homework'],
            birthday_date
        ))
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()
