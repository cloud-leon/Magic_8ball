import requests
import sqlite3
import time

def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(str(db_file + ' file not found'))
        exit()
    return conn

def get_history(id):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM questions WHERE id=?;")
    cursor.execute(command, id)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(row)

def create_tables():
    conn = get_connection('database.db')
    cursor = conn.cursor()
    users_command = ("CREATE TABLE IF NOT EXISTS users(" +
                "id integer" +
                "email text" +
                "hashed_passwords text);")
    questions_command = ("CREATE TABLE IF NOT EXISTS questions(" +
                "id integer" +
                "user_id integer"
                "question text" +
                "answer text" +
                "date text);")
    cursor.execute(users_command)
    cursor.execute(questions_command)
    conn.commit()


def insert_user(id, email, hashed_pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO users(id, email, hashed_password)" +
                "VALUES(?, ?, ?);")
    cursor.execute(command, (id, email, hashed_pswd))
    conn.commit()


def find_user(id, email, hashed_pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE id=?;")
    cursor.execute(command)
    row = cursor.fetchall()[0]
    if row[1] == email and row[2] == hashed_pswd:
        return True
    return False


def insert_question(id, user_id, question, answer, date):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO questions(id, user_id, question, answer, date)" +
                "VALUES(?, ?, ?, ?, ?);")
    cursor.execute(command, user_id, question, answer, date, id)
    conn.commit()


def is_question(question):
    question_words = ['will', 'is', 'did', 'would']
    for word in question_words:
        if word in str(question).lower():
            has_question_word = True
            break
        has_question_word = False
    if '?' not in str(question) or not has_question_word:
        print("wrong")
        return False
    return True


def get_answer(question, user):
    if not is_question(question):
        return False
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url + question)
    data = response.json()
    db_file = 'database.db'
    create_tables(db_file)
    return data['magic']['answer']

