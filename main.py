"""
Данный код выполняет следующую функцию:
1) Cчитывание json с внешенго API
2) Парсинг json
3) Создание директории, содержащей файлы с распарсенными данными

This code does the following:
1) Reading json from external API
2) json parsing
3) Creation of a directory containing files with parsed data
"""

import json
import datetime
import os
import urllib.request
import shutil


with urllib.request.urlopen('https://json.medrating.org/todos') as file:
    todos = json.load(file)
with urllib.request.urlopen('https://json.medrating.org/users') as file:
    users = json.load(file)
path = r'C:\programes\high level\TestForMedicalCompany\tasks'
os.makedirs(path, exist_ok=True)


def search_json(key, obj):  # key - ключ в словарях, являющихся obj[i] - объектами в списке, obj - список
    run = 0  # run перебирает словари в списке
    while run < len(obj):
        if key not in obj[run]:
            obj.remove(obj[run])
        else:
            run += 1


def observe_title(elem):
    if len(elem['title']) < 48:
        elem['title'] = elem['title']
    else:
        elem['title'] = elem['title'][0:48] + '...'


def parse():
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
                observe_title(tasks)
                finished_tasks.append(tasks['title'])
                sum_finished_tasks += 1
            else:
                observe_title(tasks)
                unfinished_tasks.append(tasks['title'])
                sum_unfinished_tasks += 1
                
        now = datetime.datetime.strftime(datetime.datetime.now(), "%d.%m.%Y %H:%M")
        unfinished_tasks = '\n'.join(str(value) for value in unfinished_tasks)
        finished_tasks = '\n'.join(str(value) for value in finished_tasks)
        all_tasks = sum_finished_tasks + sum_unfinished_tasks

        if os.path.isfile(rf"{path}\{users[j]['username']}.txt"):
            last_md_date = os.stat(rf"{path}\{users[j]['username']}.txt").st_mtime
            result_date = datetime.datetime.fromtimestamp(last_md_date).strftime('%Y-%m-%dT%H.%M')
            shutil.copy(rf"{path}\{users[j]['username']}.txt", rf"{path}\old{users[j]['username']}_{result_date}.txt")

        with open(rf"{path}\{users[j]['username']}.txt", 'w', encoding='utf-8') as f:
            if users[j]["name"] != 0:
                f.write(str('Отчёт для ') + str(f'{users[j]["username"]}.') + '\n' + str(users[j]["name"]) + str(
                    f' <{users[j]["email"]}> ') + str(now)[:-3] + '\n' + str(
                    f"Всего задач: {all_tasks}") + '\n' + '\n' + str(
                    f"Завершенные задачи ({sum_finished_tasks}):") + '\n' + str(
                    f"{finished_tasks}") + '\n' + '\n' + str(
                    f"Оставшиеся задачи ({sum_unfinished_tasks}):") + '\n' + str(
                    f"{unfinished_tasks}"))
        
        j += 1
        i += 1


if __name__ == "__main__":
    parse()
