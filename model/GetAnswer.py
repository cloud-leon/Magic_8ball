from ssl import AlertDescription
import requests
import sqlite3
import time

count = 0
def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(str(db_file + ' file not found'))
        exit()
    return conn


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
    cursor.excecute(users_command)
    cursor.excecute(questions_command)
    conn.commit()


def insert_user(id, email, hashed_pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO users(id, email, hashed_password)" +
                "VALUES(?, ?, ?);")
    cursor.excecute(command, (id, email, hashed_pswd))
    conn.commit()


def find_user(id, email, hashed_pswd):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE id=?;")
    cursor.excecute(command)
    row = cursor.fetchall()[0]
    if row[1] == email and row[2] == hashed_pswd:
        return True
    return False


def insert_question(id, user_id, question, answer, date):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO questions(id, user_id, question, answer, date)" +
                "VALUES(?, ?, ?, ?, ?);")
    cursor.excecute(command, user_id, question, answer, date, id)
    conn.commit()


def is_question(question):
    question_words = ['will', 'is', 'did', 'would', "who", "what", "where", "when", 
    "how", "why", "can", "may", "won't","doesn't"]
    for word in question_words:
        if word not in str(question).lower():
            has_question_word = False
            break
        has_question_word = True
    if question.strip().endswith("?") is False or not has_question_word:
        print("wrong")
        return False
    return True

<<<<<<< HEAD
def get_answer(question):
=======

def get_answer(question, user):
>>>>>>> 0fac7be69ba1ecbb9761a7c3e1ee68138d308718
    if not is_question(question):
        return False
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url + question)
    data = response.json()
    db_file = 'database.db'
    create_tables(db_file)
    return data['magic']['answer']

def update_count():
    if is_question:
        count + 1
    if count == 7:
        AlertDescription("last question for the day/session")

