"""
Данный код выполняет следующую функцию:
1) Cчитывание json с внешенго API
2) Парсинг json
3) Создание директории, содержащей файлы с распарсенными данными
"""

import json
import datetime
import os
import urllib.request


def search_json(key, obj):  # key - ключ в словарях, являющихся obj[i] - объектами в списке, obj - список
    run = 0  # run перебирает словари в списке
    while run < len(obj):
        if key not in obj[run]:
            obj.remove(obj[run])
        else:
            run += 1


def observe_title():
    if len(tasks['title']) < 48:
        tasks['title'] = tasks['title']
    else:
        tasks['title'] = tasks['title'][0:48] + '...'


with urllib.request.urlopen('https://json.medrating.org/todos') as file:
    todos = json.load(file)
with urllib.request.urlopen('https://json.medrating.org/users') as file:
    users = json.load(file)
path = r'путь к вашей папке'
os.makedirs(path, exist_ok=True)

search_json('username', users)
search_json('userId', todos)
j = 0  # j перебирает словари в списке users
i = 1  # i значения ключей username в users
while i < len(users) + 1:
    cases = [case for case in todos if case['userId'] == i]
    finished_tasks = []
    unfinished_tasks = []
    sum_finished_tasks = 0
    sum_unfinished_tasks = 0
    for tasks in cases:

        if tasks['completed']:
            observe_title()
            finished_tasks.append(tasks['title'])
            sum_finished_tasks += 1
        else:
            observe_title()
            unfinished_tasks.append(tasks['title'])
            sum_unfinished_tasks += 1
    now = datetime.datetime.strftime(datetime.datetime.now(), "%d.%m.%Y %H:%M")
    unfinished_tasks = '\n'.join(str(value) for value in unfinished_tasks)
    finished_tasks = '\n'.join(str(value) for value in finished_tasks)
    all_tasks = sum_finished_tasks + sum_unfinished_tasks
    with open(rf"{path}\{users[j]['username']}.txt", 'w', encoding='utf-8') as file:
        if users[j]["name"] != 0:
            file.write(str('Отчёт для ') + str(f'{users[j]["username"]}.') + '\n' + str(users[j]["name"]) + str(
                f' <{users[j]["email"]}> ') + str(now) + '\n' + str(
                f"Всего задач: {all_tasks}") + '\n' + '\n' + str(
                f"Завершенные задачи ({sum_finished_tasks}):") + '\n' + str(
                f"{finished_tasks}") + '\n' + '\n' + str(
                f"Оставшиеся задачи ({sum_unfinished_tasks}):") + '\n' + str(
                f"{unfinished_tasks}"))
    j += 1
    i += 1
