import requests
import json
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable
import os


def get_headhunter_vacancies(title, pages):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 (fannyfanny879@gmail.com)',
        'Accept-Language': 'ru-RU'
    }

    params = {
        'text': title,
        'area': 1,
        'page': pages,
        'per_page': 20,
        'search_period': 30
    }

    url = "https://api.hh.ru/vacancies"
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)
    response.raise_for_status()
    data = response.content.decode()
    response.close()
    return json.loads(data)


def get_superjob_vacancies(title, pages):
    headers = {
        "X-Api-App-Id": os.environ["SUPER_JOB_SECRET_KEY"],
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        'keywords': title,
        'page': pages,
        'count': 20,
        'period': 30
    }

    url = "https://api.superjob.ru/2.0/vacancies/"
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)
    response.raise_for_status()
    data = response.content.decode()
    response.close()
    return json.loads(data)


def count_headhunter_vacancies(job, pages, clue):
    count = 0
    for page in range(pages):
        vacancies = get_headhunter_vacancies(job, page)
        count += len(vacancies[clue])
    return count


def count_superjob_vacancies(job, pages, clue):
    count = 0
    for page in range(pages):
        vacancies = get_superjob_vacancies(job, page)
        count += len(vacancies[clue])
    return count


def predict_rub_salary_for_headhunter(vacancie):
    if vacancie is None or vacancie['currency'] != 'RUR':
        return
    if vacancie['from'] and vacancie['to']:
        return (vacancie['from'] + vacancie['to']) / 2


def predict_rub_salary_for_superJob(job):
    if job['payment_from'] == 0:
        return None
    return round((job['payment_from'] + job['payment_to'])/2)


def draw_table(language_name):
    table_data = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for key, value in language_name.items():
        table_data.append([key, str(value['vacancies_found']), str(value['vacancies_processed']), str(value['average_salary'])])

    return table_data


def create_dict_jobs(clue):
    language_name = {
        "Python": {},
        "Java": {},
        "JavaScript": {},
        "С++": {},
        "C#": {},
        "Ruby": {},
        "PHP": {},
        "C": {},
        "Swift": {},
        "Go": {}
    }
    for language in language_name.keys():
        programmer = "Программист {}".format(language)

        if clue == 'items':
            language_name[language]["vacancies_found"] = count_headhunter_vacancies(programmer, 4, clue)
        elif clue == 'objects':
            language_name[language]["vacancies_found"] = count_superjob_vacancies(programmer, 4, clue)

        vacancies_processed = []

        if clue == 'items':
            json_vacancies = get_headhunter_vacancies(programmer, 4)
            for vacancies in json_vacancies['items']:
                vacancies_salary = vacancies['salary']
                vacancies_processed.append(predict_rub_salary_for_headhunter(vacancies_salary))
        elif clue == 'objects':
            json_vacancies = get_superjob_vacancies(programmer, 4)
            for vacancies in json_vacancies['objects']:
                if vacancies['town']['title'] == 'Москва':
                    vacancies_processed.append(predict_rub_salary_for_superJob(vacancies))

        vacancies_proces = list(filter(lambda x: x is not None, vacancies_processed))
        language_name[language]["vacancies_processed"] = len(vacancies_proces)

        average_salery = 0
        for vacanc in vacancies_proces:
            average_salery += int(vacanc)
        if len(vacancies_proces) == 0:
            language_name[language]["average_salary"] = 0
        else:
            language_name[language]["average_salary"] = round(average_salery / len(vacancies_proces))
    return language_name


def show_table(clue, title):
    table_data = draw_table(create_dict_jobs(clue))
    table = AsciiTable(table_data, title)
    return table.table


if __name__ == "__main__":
    load_dotenv()
    print(show_table('items', 'HeadHunter Moscow'))
    print(show_table('objects', 'SuperJob Moscow'))
