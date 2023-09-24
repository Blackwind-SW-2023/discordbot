import sqlite3

conn = sqlite3.connect('bot.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS id
             (username TEXT PRIMARY KEY, id TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS password
             (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS naver_id
             (username TEXT PRIMARY KEY, naver_id TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS naver_pw
             (username TEXT PRIMARY KEY, naver_pw TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS studnumber
             (username TEXT PRIMARY KEY, studnumber TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    project_name TEXT NOT NULL,
    deadline TEXT NOT NULL,
    course_name TEXT NOT NULL,
    UNIQUE(username, project_name, deadline, course_name)
);
''')
c.execute('''CREATE TABLE IF NOT EXISTS lectures (
    lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    day_of_week INTEGER NOT NULL,
    lecture_code TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    lecture_name TEXT NOT NULL,
    location TEXT NOT NULL,
    professor_name TEXT NOT NULL,
    UNIQUE(username, day_of_week, lecture_code, start_time, end_time, lecture_name, location, professor_name)
);
''')
# c.execute('''CREATE TABLE IF NOT EXISTS lecture
#              (id TEXT PRIMARY KEY, lecture TEXT)''')

conn.commit()
conn.close()