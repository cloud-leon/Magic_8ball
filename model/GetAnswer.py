import requests
import sqlite3
from datetime import date

def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(str(db_file + ' file not found'))
        return None
    return conn

def get_history(user_id):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM questions WHERE user_id=?;")
    cursor.execute(command, (user_id,))
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(row)
    return data

def create_tables():
    conn = get_connection('database.db')
    cursor = conn.cursor()
    users_command = ("CREATE TABLE IF NOT EXISTS users(" +
                "id integer primary key autoincrement," +
                "email text," +
                "password text);")
    questions_command = ("CREATE TABLE IF NOT EXISTS questions(" +
                "id integer primary key autoincrement," +
                "user_id integer,"
                "question text," +
                "answer text," +
                "date text);")
    cursor.execute(users_command)
    cursor.execute(questions_command)
    conn.commit()


def insert_user(email, pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO users(email, password)" +
                "VALUES(?, ?);")
    cursor.execute(command, (email, pswd))
    conn.commit()


def find_user(email, pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE email=?;")
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    row = rows[0]
    if row[1] == email and row[2] == pswd:
        return row[0]
    return False


def user_exists(email):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE email=?;")
    cursor.execute(command, (email,))
    if len(cursor.fetchall()) > 0:
        return True
    return False


def insert_question(user_id, question, answer):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO questions(user_id, question, answer, date)" +
                "VALUES(?, ?, ?, ?);")
    cursor.execute(command, (user_id, question, answer, date.today()))
    conn.commit()


def is_question(question):
    question_words = ['will', 'is', 'did', 'would', 'should', 'does']
    for word in question_words:
        if word in str(question).lower():
            has_question_word = True
            break
        has_question_word = False
    print(has_question_word)
    return has_question_word


def get_answer(question):
    if not is_question(question):
        return 'This is not a valid question'
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url + question)
    data = response.json()
    create_tables()
    return data['magic']['answer']

