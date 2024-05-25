import streamlit as st
import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='Dormitory', user='*',
                        host='localhost', password='*')

cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

st.code("1. Знайти імена гуртожитків у який такий самий набір\n\tімен кімнат, як і в гуртожитку з id X", language="sql")
with st.form("query1"):
    query1 = '''
SELECT d1.name
FROM dormitories d1
WHERE d1.id <> X
  AND (
    SELECT COUNT(DISTINCT r1."room_name")
    FROM rooms r1
    WHERE r1."dormitoryId" = d1.id
  ) = (
    SELECT COUNT(DISTINCT r2."room_name")
    FROM rooms r2
    WHERE r2."dormitoryId" = X
  )
  AND NOT EXISTS (
    SELECT 1
    FROM rooms r2
    WHERE r2."dormitoryId" = X
    AND NOT EXISTS (
      SELECT 1
      FROM rooms r1
      WHERE r1."dormitoryId" = d1.id
        AND r1."room_name" = r2."room_name"
    )
  );
    '''

    st.code(query1, language="sql")
    X = st.number_input("dormitoryId X:", step=1, min_value=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
    SELECT d1.name
    FROM dormitories d1
    WHERE d1.id <> {X}
      AND (
        SELECT COUNT(DISTINCT r1."room_name")
        FROM rooms r1
        WHERE r1."dormitoryId" = d1.id
      ) = (
        SELECT COUNT(DISTINCT r2."room_name")
        FROM rooms r2
        WHERE r2."dormitoryId" = {X}
      )
      AND NOT EXISTS (
        SELECT 1
        FROM rooms r2
        WHERE r2."dormitoryId" = {X}
        AND NOT EXISTS (
          SELECT 1
          FROM rooms r1
          WHERE r1."dormitoryId" = d1.id
            AND r1."room_name" = r2."room_name"
        )
      );

    ''')
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))


st.code("2. Знайти гуртожитки, які не містять жодного студента з таким самим \n\tім'ям і прізвищем, як і гуртожиток з імʼям X: ", language="sql")
with st.form("query2"):
    query2 = '''
        SELECT d.name AS dormitory_name
        FROM Dormitories d
        WHERE NOT EXISTS (
            SELECT 1
            FROM Rooms r
            JOIN students s ON r.id = s."roomId"
            WHERE r."dormitoryId" = d.id
            AND CONCAT(s.name, ' ', s.surname) IN (
                SELECT CONCAT(s2.name, ' ', s2.surname)
                FROM Dormitories d2
                JOIN Rooms r2 ON d2.id = r2."dormitoryId"
                JOIN students s2 ON r2.id = s2."roomId"
                WHERE d2.name = 'X'
            )
        );
    '''

    st.code(query2, language="sql")
    X = st.text_input("dorm name X:")
    data = (X, )
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
        SELECT d.name AS dormitory_name
        FROM Dormitories d
        WHERE NOT EXISTS (
            SELECT 1
            FROM Rooms r
            JOIN students s ON r.id = s."roomId"
            WHERE r."dormitoryId" = d.id
            AND CONCAT(s.name, ' ', s.surname) IN (
                SELECT CONCAT(s2.name, ' ', s2.surname)
                FROM Dormitories d2
                JOIN Rooms r2 ON d2.id = r2."dormitoryId"
                JOIN students s2 ON r2.id = s2."roomId"
                WHERE d2.name = (%s)
            )
        );
        ''', data)
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))

st.code("3. Знайти студентів гуртожитку з номером X, які мають таких же відвідувачів як і студент з іменем і прізвищем Y", language="sql")
with st.form("query3"):
    query3 = '''
       WITH y_student_id AS (
            SELECT id
            FROM Students s
            WHERE dormitory_num = {X} AND CONCAT(s.name, ' ' , s.surname) = '{Y}'
       )
       (
        SELECT s.name AS name, s.surname as surname
        FROM Students s
        WHERE s.dormitory_num = {X}
        AND CONCAT(s.name, ' ', s.surname) <> '{Y}'
        AND NOT EXISTS (
            SELECT 1
            FROM student_visitors sv
            WHERE sv."studentId" = s.id
            AND sv."visitorId" NOT IN (
                SELECT sv."visitorId"
                FROM student_visitors sv
                WHERE sv."studentId" = (SELECT id FROM y_student_id)
            )
        )
        AND EXISTS (
            SELECT "studentId"
            from student_visitors
            where "studentId" = s.id
        )
       );
    '''

    st.code(query3, language="sql")
    X = st.number_input("dormitory number X:", step=1, min_value=1)
    Y = st.text_input("student name surname Y:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        cursor.execute(f'''
       WITH y_student_id AS (
            SELECT id
            FROM Students s
            WHERE dormitory_num = {X} AND CONCAT(s.name, ' ' , s.surname) = '{Y}'
       )
       (
        SELECT s.name AS name, s.surname as surname
        FROM Students s
        WHERE s.dormitory_num = {X}
        AND CONCAT(s.name, ' ', s.surname) <> '{Y}'
        AND NOT EXISTS (
            SELECT 1
            FROM student_visitors sv
            WHERE sv."studentId" = s.id
            AND sv."visitorId" NOT IN (
                SELECT sv."visitorId"
                FROM student_visitors sv
                WHERE sv."studentId" = (SELECT id FROM y_student_id)
            )
        )
        AND EXISTS (
            SELECT "studentId"
            from student_visitors
            where "studentId" = s.id
        )
       );
        ''')
        data = cursor.fetchall()
        st.dataframe(pd.DataFrame(data))
