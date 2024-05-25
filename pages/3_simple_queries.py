import streamlit as st
import psycopg2
import psycopg2.extras
import pandas as pd

conn = psycopg2.connect(dbname='Dormitory', user='*',
                        host='localhost', password='*')


cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

st.code("1. Знайти всі кімнати гуртожитку, з номером X :", language="sql")
with st.form("query1"):
    query1 = '''
    SELECT * FROM Rooms
    WHERE \"dormitoryId\" =
      (SELECT id FROM Dormitories
      WHERE Dormitories.dorm_number = X);
    '''
    st.code(query1, language="sql")
    X = st.number_input("dorm number X:", min_value=1, step=1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(
            f"SELECT * FROM Rooms WHERE \"dormitoryId\" = (SELECT id FROM Dormitories WHERE Dormitories.dorm_number = {X});")
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))

st.code('''2. Знайти імена всіх студентів, з номером гуртожитку X
        і балансом менше ніж Y :''')
with st.form("query2"):
    query2 = '''
    SELECT s.name, s.surname
    FROM Students AS s
    WHERE s.dormitory_num = X
    AND s.id IN (
      SELECT "studentId"
      FROM Accounts AS a
      WHERE a.balance < Y
    );
    '''
    st.code(query2, language="sql")
    X = st.number_input("dorm number X:", min_value=1, step=1)
    Y = st.number_input("balance < Y: ")

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(
            f"SELECT s.name, s.surname FROM Students AS s WHERE s.dormitory_num = {X} AND s.id IN ( SELECT \"studentId\" FROM Accounts AS a WHERE a.balance < {Y});")
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))

st.code('''3. Знайти імена всіх студентів, які проживають у гуртожитку номер X,
        у яких наразі є відвідувачі :''', language="sql")
with st.form("query3"):
    query3 = '''
    SELECT s.surname, s.name
    FROM Students s
    WHERE s.dormitory_num = X
    AND s.id IN (
      SELECT s.id
      FROM students s
      INNER JOIN student_visitors sv ON s.id = sv."studentId"
      WHERE sv.time_out IS NULL
    );
    '''
    st.code(query3, language="sql")
    X = st.number_input("dorm number X:", min_value=1, step=1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(
            f"SELECT s.surname, s.name FROM Students s where s.dormitory_num = {X} and s.id in ( select s.id from students s INNER JOIN student_visitors sv ON s.id = sv.\"studentId\" WHERE sv.time_out IS NULL);")
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))

# st.code("4. Знайти середню кількість вільних місць у кімнатах у кожному гуртожитку :", language="sql")
# with st.form("query4"):
#     query4 = '''
#     SELECT d.name  AS dormitory_name, AVG(r.free_capacity) AS average_free_capacity
#     FROM Rooms AS r
#     INNER JOIN Dormitories AS d ON r."dormitoryId"  = d.id
#     GROUP BY d.name ;
#     '''
#     st.code(query4, language="sql")
#
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         cursor.execute(f"SELECT d.name  AS dormitory_name, AVG(r.free_capacity) AS average_free_capacity FROM Rooms AS r INNER JOIN Dormitories AS d ON r.\"dormitoryId\" = d.id GROUP BY d.name;")
#         data = cursor.fetchall()
#         st.dataframe(pd.DataFrame(data))

st.code("4. Знайти кількість вільних місць у кімнатах гуртожитку з імʼям X:", language="sql")
with st.form("query4"):
    query4 = '''
        SELECT SUM(free_capacity) AS total_free_capacity FROM Dormitories d1
        INNER JOIN Rooms r1 on d1.name = 'X' AND d1.id = r1."dormitoryId";
    '''
    st.code(query4, language="sql")
    X = st.text_input("dorm name X:")

    submitted = st.form_submit_button("Submit")
    if submitted:
        data = (X, )
        cursor.execute('''
        SELECT SUM(free_capacity) FROM Dormitories d1
        INNER JOIN Rooms r1 on d1.name = (%s) and d1.id = r1."dormitoryId";
            ''', data)
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))

st.code('''5. Знайти для гуртожитку з номером X кількість відвідувачів,
        які побували в гуртожитоку за останній місяць.''')
with st.form("query5"):
    query5 = '''
    SELECT
        COUNT(DISTINCT sv."visitorId") AS visitor_count
    FROM student_visitors sv
    WHERE sv."studentId" IN (
        SELECT id FROM students WHERE dormitory_num = X
    )
    AND sv.time_in >= CURRENT_DATE - INTERVAL '1 MONTH';
    '''
    st.code(query5, language="sql")
    X = st.number_input("dorm number X:", value=1, step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        if X < 1:
            st.warning("Номер гуртожитку має бути >= 1")
        else:
            cursor.execute(f'''
            SELECT
                COUNT(DISTINCT sv."visitorId") AS visitor_count
            FROM student_visitors sv
            WHERE sv."studentId" IN (
                select id from students where dormitory_num = {X}
            )
            AND sv.time_in >= CURRENT_DATE - INTERVAL '1 MONTH';
            ''')
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data))
