import streamlit as st
import psycopg2
import psycopg2.extras
import pandas as pd

conn = psycopg2.connect(dbname='Dormitory', user='*',
                        host='localhost', password='*')


cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


tables = ["dormitories", "rooms", "students", "accounts",
          "workers", "visitors", "student_visitors"]

selected_table = st.selectbox("Виберіть таблицю", tables)

cursor.execute(f"SELECT * FROM {selected_table}")
data = cursor.fetchall()
if len(data) > 0:
    st.dataframe(pd.DataFrame(data))
else:
    st.write("Таблиця порожня")

cursor.close()
conn.close()
