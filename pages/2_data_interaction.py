import streamlit as st
import psycopg2
from psycopg2 import IntegrityError
import psycopg2.extras

conn = psycopg2.connect(dbname='Dormitory', user='*',
                        host='localhost', password='*')

cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

st.title("Управління Гуртожитками")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Гуртожитки", "Кімнати", "Студенти", "Працівники", "Відвідувачі"])

with tab1:
    st.header("Дії :")

    # subtab1, subtab2, subtab3 = st.tabs(["Додати Гуртожиток", "Видалити Гуртожиток", "Оновити Гуртожиток"])
    subtab1, subtab2 = st.tabs(["Додати Гуртожиток", "Оновити Гуртожиток"])

    with subtab1:
        st.subheader("Додати Гуртожиток")
        dorm_name = st.text_input(
            "Назва Гуртожитку", placeholder="Гуртожиток *")
        dorm_number = st.number_input("Номер Гуртожитку", min_value=1)
        dorm_address = st.text_input("Адреса Гуртожитку")

        if st.button("Додати Гуртожиток"):
            if not dorm_name or not dorm_number or not dorm_address:
                st.warning("Заповніть всі поля")
            else:
                cursor.execute(
                    "INSERT INTO dormitories (name, dorm_number, address, \"createdAt\", \"updatedAt\") VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                    (dorm_name, dorm_number, dorm_address)
                )
                conn.commit()
                st.success(f"Гуртожиток '{dorm_name}' успішно додано!")

    # with subtab2:
    #     st.subheader("Видалити Гуртожиток")
    #     cursor.execute("SELECT id, name FROM dormitories")
    #     dormitories = cursor.fetchall()
    #     dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
    #
    #     if dormitory_options:
    #         dorm_to_delete = st.selectbox(
    #             "Виберіть Гуртожиток для Видалення", options=dormitory_options.keys())
    #         if st.button("Видалити Гуртожиток"):
    #             dorm_id = dormitory_options[dorm_to_delete]
    #             cursor.execute(
    #                 "DELETE FROM dormitories WHERE id = %s", (dorm_id,))
    #             conn.commit()
    #             st.success(f"Гуртожиток '{dorm_to_delete}' успішно видалено!")
    #     else:
    #         st.warning(
    #             "Список гуртожитків порожній. Немає гуртожитків для видалення.")Списокт

    with subtab2:
        st.subheader("Оновити Гуртожиток")
        cursor.execute("SELECT id, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
        if dormitory_options:
            dorm_to_update = st.selectbox(
                "Виберіть Гуртожиток для Оновлення", options=dormitory_options.keys())
            st.divider()
            if dorm_to_update:
                dorm_id = dormitory_options[dorm_to_update]
                cursor.execute(
                    "SELECT * FROM dormitories WHERE id = %s", (dorm_id,))
                dorm = cursor.fetchone()
                updated_name = st.text_input(
                    "Оновлена Назва", value=dorm['name'])
                updated_number = st.number_input(
                    "Оновлений Номер", min_value=1, value=dorm['dorm_number'])
                updated_address = st.text_input(
                    "Оновлена Адреса", value=dorm['address'])

                if st.button("Оновити Гуртожиток"):
                    if not updated_name or not updated_number or not updated_address:
                        st.warnging("Заповніть всі поля")
                    else:
                        cursor.execute(
                            "UPDATE dormitories SET name = %s, dorm_number = %s, address = %s, \"updatedAt\" = CURRENT_TIMESTAMP WHERE id = %s",
                            (updated_name, updated_number, updated_address, dorm_id)
                        )
                        conn.commit()
                        st.success(
                            f"Гуртожиток '{updated_name}' успішно оновлено!")
        else:
            st.warning(
                "Немає жодного гуртожитку")


with tab2:
    # st.header("Дії:")

    # subtab1, subtab2 = st.tabs(["Додати Кімнату", "Видалити Кімнату"])
    # subtab1, subtab2 = st.tabs(["Додати Кімнату", "Видалити Кімнату"])

    # with subtab1:
    cursor.execute("SELECT id, name FROM dormitories")
    dormitories = cursor.fetchall()
    dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
    st.subheader("Додати Кімнату")
    dormitory_for_room = st.selectbox(
        "Виберіть Гуртожиток", options=dormitory_options.keys())
    st.divider()
    room_block_number = st.number_input("Номер Блоку", value=100)
    room_capacity = st.number_input("Місткість", value=1)
    room_name = str(room_block_number) + '/' + str(room_capacity)
    cursor.execute("SELECT id, name FROM dormitories")
    dormitories = cursor.fetchall()
    dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}

    if not dormitory_options:
        st.warning("Немає жодного гуртожитку")
    else:
        if st.button("Додати Кімнату"):
            if not room_block_number or not room_capacity:
                st.warning("Заповніть всі поля")
            elif room_block_number < 100:
                st.warning("Номер блоку не може бути менше 100")
            elif room_capacity < 1:
                st.warning("Місткість кімнати не може бути менша за 1")
            else:
                dormitory_id = dormitory_options[dormitory_for_room]
                cursor.execute(
                    "INSERT INTO rooms (block_number, capacity, free_capacity, room_name, \"dormitoryId\", \"createdAt\", \"updatedAt\") VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                    (room_block_number, room_capacity,
                     room_capacity, room_name, dormitory_id)
                )
                conn.commit()
                st.success(f"Кімнату {room_name} успішно додано!")

    # with subtab2:
    #     st.subheader("Видалити Кімнату")
    #     cursor.execute("SELECT id, name FROM dormitories")
    #     dormitories = cursor.fetchall()
    #     dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
    #
    #     dormitory_to_delete_room_from = st.selectbox("Виберіть Гуртожиток для видалення кімнати:", options=dormitory_options.keys())
    #     dormitory_id = dormitory_options[dormitory_to_delete_room_from]
    #
    #     cursor.execute("SELECT id, room_name FROM rooms WHERE \"dormitoryId\" = (%s)", (dormitory_id, ))
    #     rooms = cursor.fetchall()
    #     rooms_options = {room['room_name']: room['id'] for room in rooms}
    #
    #     if rooms_options:
    #         room_to_delete = st.selectbox("Виберіть Кімнату для Видалення", options=rooms_options.keys())
    #         if st.button("Видалити Кімнату"):
    #             room_id = rooms_options[room_to_delete]
    #             cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
    #             conn.commit()
    #             st.success(f"Кімнату '{room_to_delete}' успішно видалено!")
    #     else:
    #         st.warning("У вибраному гуртожитку немає кімнат.")

with tab3:
    st.header("Дії:")

    # subtab1, subtab2, subtab3 = st.tabs(["Додати Студента", "Видалити Студента", "Оновити Студента"])
    subtab1, subtab2 = st.tabs(["Додати Студента", "Оновити Студента"])

    with subtab1:
        st.subheader("Додати Студента")

        cursor.execute("SELECT id, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
        selected_dormitory = st.selectbox(
            "Виберіть Гуртожиток для поселення студента", options=dormitory_options.keys())
        dormitory_id = dormitory_options.get(selected_dormitory)

        if not dormitory_id:
            st.warning("Немає жоного гуртожитку")
        else:
            cursor.execute(
                "SELECT id, room_name FROM rooms WHERE free_capacity >= 1 AND \"dormitoryId\" = %s", (dormitory_id,))
            rooms = cursor.fetchall()
            room_options = {room['room_name']: room['id'] for room in rooms}

            if room_options:
                selected_room = st.selectbox(
                    "Виберіть Кімнату для поселення студента", options=room_options.keys())
                room_id = room_options[selected_room]

                student_name = st.text_input("Ім'я Студента")
                student_surname = st.text_input("Прізвище Студента")
                student_contact_info = st.text_input(
                    "Контактна Інформація Студента", value="")

                if st.button("Додати Студента"):
                    if not student_name or not student_surname:
                        st.warning(
                            "Імʼя і прізвище студента має бути заповнене")
                    else:
                        cursor.execute("""
                            SELECT d1.dorm_number FROM rooms r1
                            INNER JOIN dormitories d1 ON r1.id = %s AND d1.id = r1."dormitoryId" 
                        """, (room_id,))
                        dorm_number = cursor.fetchone()['dorm_number']

                        # Decrease free_capacity in the selected room by 1
                        cursor.execute(
                            "UPDATE rooms SET free_capacity = free_capacity - 1 WHERE id = %s", (room_id,))

                        cursor.execute("""
                            INSERT INTO students (name, surname, "roomId", contact_info, dormitory_num, "createdAt", "updatedAt")
                            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                            RETURNING id
                        """, (student_name, student_surname, room_id, student_contact_info, dorm_number))
                        student_id = cursor.fetchone()['id']

                        cursor.execute("""
                            INSERT INTO accounts ("studentId", balance, last_update_date, "createdAt", "updatedAt")
                            VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """, (student_id, 0))
                        conn.commit()
                        st.success(
                            f"Студент {student_name} {student_surname} успішно додано та рахунок створено!")
            else:
                st.warning("У вибраному гуртожитку немає кімнат для вибору.")

    # with subtab2:
    #     st.subheader("Видалити Студента")
    #
    #     cursor.execute("SELECT dorm_number, name FROM dormitories")
    #     dormitories = cursor.fetchall()
    #     dormitory_options = {dorm['name']: dorm['dorm_number'] for dorm in dormitories}
    #     selected_dormitory = st.selectbox("Виберіть Гуртожиток для видалення студента", options=dormitory_options.keys())
    #     dormitory_num = dormitory_options[selected_dormitory]
    #
    #     cursor.execute("SELECT id, name, surname FROM students WHERE dormitory_num = %s", (dormitory_num,))
    #     students = cursor.fetchall()
    #     student_options = {f"{student['name']} {student['surname']}": student['id'] for student in students}
    #
    #     if student_options:
    #         student_to_delete = st.selectbox("Виберіть Студента для Видалення", options=student_options.keys())
    #
    #         if st.button("Видалити Студента"):
    #             student_id = student_options[student_to_delete]
    #             cursor.execute("SELECT \"roomId\" FROM students WHERE id = %s", (student_id,))
    #             room_id = cursor.fetchone()['roomId']
    #             cursor.execute("UPDATE rooms SET free_capacity = free_capacity + 1 WHERE id = %s", (room_id,))
    #             cursor.execute("DELETE FROM accounts WHERE \"studentId\" = %s", (student_id,))
    #             cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    #
    #             conn.commit()
    #             st.success(f"Студента {student_to_delete} та його рахунок успішно видалено, і місце в кімнаті відновлено!")
    #     else:
    #         st.warning("У вибраному гуртожитку немає студентів для вибору.")

    with subtab2:
        st.subheader("Оновити Дані Студента")
        cursor.execute("SELECT dorm_number, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['dorm_number']
                             for dorm in dormitories}
        if not dormitory_options:
            st.warning("Немає жодного гуртожитку")

        else:
            selected_dormitory = st.selectbox(
                "Виберіть Гуртожиток для зміни даних студента", options=dormitory_options.keys())
            dormitory_num = dormitory_options[selected_dormitory]

            cursor.execute(
                "SELECT id, name, surname FROM students WHERE dormitory_num = %s", (dormitory_num,))
            students = cursor.fetchall()
            student_options = {
                f"{student['name']} {student['surname']}": student['id'] for student in students}

            if student_options:
                student_to_update = st.selectbox(
                    "Виберіть Студента для Оновлення", options=student_options.keys())
                student_id = student_options[student_to_update]

                cursor.execute(
                    "SELECT * FROM students WHERE id = %s", (student_id,))
                student = cursor.fetchone()

                new_student_name = st.text_input(
                    "Нове Ім'я Студента", value=student['name'])
                new_student_surname = st.text_input(
                    "Нове Прізвище Студента", value=student['surname'])
                new_student_contact_info = st.text_input(
                    "Нова Контактна Інформація", value=student['contact_info'])

                cursor.execute(
                    "SELECT balance FROM accounts WHERE \"studentId\" = %s", (student_id,))
                account = cursor.fetchone()
                current_balance = float(account['balance'])

                new_balance = st.number_input(
                    "Новий Баланс", value=current_balance, min_value=0.0, step=0.01)

                if st.button("Оновити Дані Студента"):
                    if not student_name or not student_surname:
                        st.warning(
                            "Імʼя, прізвище і баланс студента має бути заповнене")
                    else:
                        cursor.execute("""
                                UPDATE students
                                SET name = %s, surname = %s, contact_info = %s, \"updatedAt\" = CURRENT_TIMESTAMP
                                WHERE id = %s
                            """, (new_student_name, new_student_surname, new_student_contact_info, student_id))
                        cursor.execute("""
                                UPDATE accounts
                                SET balance = %s, last_update_date = NOW(), \"updatedAt\" = NOW()
                                WHERE \"studentId\" = %s
                            """, (new_balance, student_id))
                        conn.commit()
                        st.success(
                            f"Дані студента {student_to_update} успішно оновлено!")
            else:
                st.warning(
                    "У вибраному гуртожитку немає студентів для вибору.")

with tab4:
    # subtab1, subtab2, subtab3 = st.tabs(["Додати Працівника", "Видалити Працівника", "Оновити Дані Працівника"])
    subtab1, subtab2 = st.tabs(
        ["Додати Працівника", "Оновити Дані Працівника"])

    with subtab1:
        st.subheader("Додати Працівника")
        cursor.execute("SELECT id, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
        if not dormitory_options:
            st.warning("Немає дожного гуртожитку")
        else:
            selected_dormitory = st.selectbox(
                "Виберіть Гуртожиток для додавання працівника", options=dormitory_options.keys())
            dormitory_id = dormitory_options[selected_dormitory]

            new_worker_name = st.text_input("Ім'я Працівника")
            new_worker_surname = st.text_input("Прізвище Працівника")
            new_worker_salary = st.number_input(
                "Зарплата", value=10000.0, step=0.01)
            new_worker_position = st.text_input("Посада")

            if st.button("Додати Працівника"):
                if not new_worker_name or not new_worker_surname or not new_worker_position or not new_worker_salary:
                    st.warning("Заповніть всі поля")
                elif new_worker_salary <= 0:
                    st.warning("Зарплата має бути більше нуля")
                else:
                    cursor.execute("""
                        INSERT INTO workers (name, surname, salary, position, \"dormitoryId\", \"createdAt\", \"updatedAt\")
                        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """, (new_worker_name, new_worker_surname, new_worker_salary, new_worker_position, dormitory_id))
                    conn.commit()
                    st.success(
                        f"Працівника {new_worker_name} {new_worker_surname} успішно додано!")

    # with subtab2:
    #     st.subheader("Видалити Працівника")
    #     cursor.execute("SELECT id, name FROM dormitories")
    #     dormitories = cursor.fetchall()
    #     dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
    #     selected_dormitory = st.selectbox("Виберіть Гуртожиток для видалення працівника", options=dormitory_options.keys())
    #     dormitory_id = dormitory_options[selected_dormitory]
    #
    #     cursor.execute("SELECT id, name, surname FROM workers WHERE \"dormitoryId\" = %s", (dormitory_id,))
    #     workers = cursor.fetchall()
    #     worker_options = {f"{worker['name']} {worker['surname']}": worker['id'] for worker in workers}
    #
    #     if worker_options:
    #         worker_to_delete = st.selectbox("Виберіть Працівника для Видалення", options=worker_options.keys())
    #
    #         if st.button("Видалити Працівника"):
    #             worker_id = worker_options[worker_to_delete]
    #             cursor.execute("DELETE FROM workers WHERE id = %s", (worker_id,))
    #             conn.commit()
    #             st.success(f"Працівника {worker_to_delete} успішно видалено!")
    #     else:
    #         st.warning("У вибраному гуртожитку немає працівників для вибору.")

    with subtab2:
        st.subheader("Оновити Дані Працівника")
        cursor.execute("SELECT id, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['id'] for dorm in dormitories}
        if not dormitory_options:
            st.warning("Немає жодного гуртожитку")
        else:
            selected_dormitory = st.selectbox(
                "Виберіть Гуртожиток для оновлення даних працівника", options=dormitory_options.keys())
            dormitory_id = dormitory_options[selected_dormitory]

            cursor.execute(
                "SELECT id, name, surname FROM workers WHERE \"dormitoryId\" = %s", (dormitory_id,))
            workers = cursor.fetchall()
            worker_options = {
                f"{worker['name']} {worker['surname']}": worker['id'] for worker in workers}

            if worker_options:
                worker_to_update = st.selectbox(
                    "Виберіть Працівника для Оновлення", options=worker_options.keys())
                worker_id = worker_options[worker_to_update]

                cursor.execute(
                    "SELECT * FROM workers WHERE id = %s", (worker_id,))
                worker = cursor.fetchone()

                new_worker_name = st.text_input(
                    "Нове Ім'я Працівника", value=worker['name'])
                new_worker_surname = st.text_input(
                    "Нове Прізвище Працівника", value=worker['surname'])
                new_worker_salary = st.number_input("Нова Зарплата", value=float(
                    worker['salary']), min_value=0.0, step=0.01)
                new_worker_position = st.text_input(
                    "Нова Посада", value=worker['position'])

                if st.button("Оновити Дані Працівника"):
                    if not new_worker_name or not new_worker_surname or not new_worker_position or not new_worker_salary:
                        st.warning("Заповніть всі поля")
                    else:
                        cursor.execute("""
                            UPDATE workers
                            SET name = %s, surname = %s, salary = %s, position = %s, \"updatedAt\" = CURRENT_TIMESTAMP
                            WHERE id = %s
                        """, (new_worker_name, new_worker_surname, new_worker_salary, new_worker_position, worker_id))
                        conn.commit()
                        st.success(
                            f"Дані працівника {worker_to_update} успішно оновлено!")
            else:
                st.warning(
                    "У вибраному гуртожитку немає працівників для вибору.")

    with tab5:
        st.subheader("Додати Відвідувача")

        cursor.execute("SELECT dorm_number, name FROM dormitories")
        dormitories = cursor.fetchall()
        dormitory_options = {dorm['name']: dorm['dorm_number']
                             for dorm in dormitories}

        if not dormitory_options:
            st.warning("Немає жодного гуртожитку")
        else:
            selected_dormitory = st.selectbox(
                "Виберіть Гуртожиток для додавання відвідувача", options=dormitory_options.keys())
            dormitory_num = dormitory_options[selected_dormitory]

            cursor.execute(
                "SELECT id, name, surname FROM students WHERE \"dormitory_num\" = %s", (dormitory_num,))
            students = cursor.fetchall()
            if students:
                student_options = {
                    f"{student['name']} {student['surname']}": student['id'] for student in students}
                selected_student = st.selectbox(
                    "Виберіть Студента", options=student_options.keys())
                student_id = student_options[selected_student]

                new_visitor_name = st.text_input("Ім'я Відвідувача")
                new_visitor_surname = st.text_input("Прізвище Відвідувача")
                new_visitor_passport = st.text_input(
                    "Паспортні Дані Відвідувача")

                if st.button("Додати Відвідувача"):
                    if not new_visitor_name or not new_visitor_surname or not new_visitor_passport:
                        st.warning("Заповніть всі поля")
                    else:
                        cursor.execute("""
                            SELECT id FROM visitors
                            WHERE name = %s AND surname = %s AND passport = %s
                        """, (new_visitor_name, new_visitor_surname, new_visitor_passport, ))
                        existing_visitor = cursor.fetchone()

                        if existing_visitor:
                            visitor_id = existing_visitor['id']
                        else:
                            try:
                                cursor.execute("""
                                    INSERT INTO visitors (name, surname, passport, \"createdAt\", \"updatedAt\")
                                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                                    RETURNING id
                                """, (new_visitor_name, new_visitor_surname, new_visitor_passport,))
                                visitor_id = cursor.fetchone()['id']

                                if visitor_id:
                                    cursor.execute("""
                                    INSERT INTO student_visitors (\"studentId\", \"visitorId\", time_in, \"createdAt\", \"updatedAt\")
                                    VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                                """, (student_id, visitor_id,))
                                    conn.commit()
                                    st.success(
                                        f"Відвідувача {new_visitor_name} {new_visitor_surname} успішно додано для студента {selected_student}!")
                                else:
                                    st.warning(
                                        "Не вдалося створити відвідувача")
                            except IntegrityError:
                                st.warning(
                                    "Відвудувач з такими паспортними даними існує, спробуйте ще раз")
                                pass

            else:
                st.warning("У вибраному гуртожитку немає студентів.")

cursor.close()
conn.close()
