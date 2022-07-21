import requests
import pprint


def is_question(question):
    question_words = ['will', 'is', 'did', 'would']
    for word in question_words:
        if word not in str(question).lower():
            has_question_word = False
            break
        has_question_word = True
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
    pprint.pprint(data)
    return data['magic']

