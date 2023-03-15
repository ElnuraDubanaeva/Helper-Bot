import sqlite3


def create_sql():
    global db, cursor
    db = sqlite3.connect("toefl.sqlite3")
    cursor = db.cursor()
    if db:
        print("Data Base connected")
    db.execute(
        """CREATE TABLE IF NOT EXISTS students_info
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  data_time DATETIME,   
                  student_fullname VARCHAR(50),
                  student_number INTEGER(10),
                  student_city VARCHAR(10),
                  student_level VARCHAR(15),
                  student_test VARCHAR(15),
                  student_age INTEGER,
                  student_username VARCHAR(18),
                  test TEXT
                  speaking INTEGER,
                  listening INTEGER,
                  writing INTEGER,
                  reading INTEGER,
                  total INTEGER)"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS tests_done
                  (id INTEGER PRIMARY KEY AUTOINCREMENT ,
                  data_time DATETIME,   
                  student_fullname VARCHAR(50),
                  student_number INTEGER(10),
                  student_city VARCHAR(10),
                  student_level VARCHAR(15),
                  student_test VARCHAR(15),
                  student_age INTEGER,
                  student_username VARCHAR(18),
                  test TEXT,
                  speaking INTEGER,
                  listening INTEGER,
                  writing INTEGER,
                  reading INTEGER,
                  total INTEGER)"""
    )
    db.commit()


async def insert_sql(state):
    async with state.proxy() as data:
        cursor.execute(
            "INSERT INTO students_info(data_time,student_fullname,student_number,student_city,student_level,student_test,student_age,student_username) "
            "VALUES(CURRENT_DATE,?,?,?,?,?,?,?)",
            tuple(data.values()),
        )
    db.commit()


async def all_sql():
    return cursor.execute("SELECT * FROM students_info").fetchall()


async def today_students():
    return cursor.execute("SELECT * FROM students_info WHERE data_time = CURRENT_DATE")


async def delete_sql(id_):
    cursor.execute("DELETE FROM students_info WHERE id = ? ", (id_,))
    db.commit()


async def update_test(data_time, id_):
    cursor.execute("UPDATE students_info SET test = ? WHERE id = ? ", (data_time, id_))
    db.commit()


async def get_fullname(name_id_):
    fullname = cursor.execute(
        "SELECT student_fullname FROM students_info WHERE id = ?", (name_id_,)
    ).fetchone()
    return fullname


async def students_test():
    return cursor.execute("SELECT * FROM students_info WHERE test NOT NULL")


async def get_data_to_test_done(test_done_id):
    cursor.execute(
        """INSERT INTO tests_done (data_time,student_fullname,student_number,student_city,student_level,student_test,student_age,student_username,test)
    SELECT data_time,student_fullname,student_number,student_city,student_level,student_test,student_age,student_username,test FROM students_info WHERE id = ? """,
        (test_done_id,),
    )
    db.commit()


async def get_all_test_done():
    return cursor.execute("""SELECT * FROM tests_done""").fetchall()


async def insert_test_done(speaking, listening, writing, reading, total, id_test):
    cursor.execute(
        "UPDATE tests_done SET speaking=? ,listening=?, writing=?,reading=?,total=? WHERE id = ?",
        (speaking, listening, writing, reading, total, id_test),
    )
    db.commit()


async def get_results_bd():
    return cursor.execute(
        """SELECT * FROM tests_done WHERE (total NOT NULL)"""
    ).fetchall()
