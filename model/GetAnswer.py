import requests
import sqlite3

def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(str(db_file + ' file not found'))
        exit()
    return conn


def create_tables(db_file):
    conn = get_connection(db_file)
    cursor = conn.cursor()
    users_command = ("CREATE TABLE IF NOT EXISTS users(" +
                "id integer" +
                "username text" +
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


def insert_user(db_file, id, username, hashed_pswd):
    conn = get_connection(db_file)
    cursor = conn.cursor()
    command = ("UPDATE users" +
                "SET username = ? ," +
                "hashed_password = ?" +
                "WHERE id = ?;")
    cursor.excecute(command, (username, hashed_pswd, id))
    conn.commit()


def insert_question(db_file, id, user_id, question, answer, date):
    conn = get_connection(db_file)
    cursor = conn.cursor()
    command = ("UPDATE questions" +
                "SET user_id = ? ," +
                "question = ? ," +
                "answer = ? ," +
                "date = ?" +
                "WHERE id = ?;")
    cursor.excecute(command, user_id, question, answer, date, id)
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


def get_answer(question):
    if not is_question(question):
        exit()
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url + question)
    data = response.json()
    return data['magic']

