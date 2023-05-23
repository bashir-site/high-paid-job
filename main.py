import requests
import json
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable
import os


def get_headhunter_vacancies(title, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 (fannyfanny879@gmail.com)',
        'Accept-Language': 'ru-RU'
    }

    params = {
        'text': title,
        'area': 1,
        'page': page,
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


def get_superjob_vacancies(title, page):
    headers = {
        "X-Api-App-Id": os.environ["SUPER_JOB_SECRET_KEY"],
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        'keywords': title,
        'page': page,
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
    table = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, description in language_name.items():
        table.append([language, str(description['vacancies_found']), str(description['vacancies_processed']), str(description['average_salary'])])

    return table


def collect_vacancies_from_api(clue):
    language_names = {
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
    for language in language_names.keys():
        programmer = "Программист {}".format(language)

        if clue == 'items':
            language_names[language]["vacancies_found"] = count_headhunter_vacancies(programmer, 4, clue)
        elif clue == 'objects':
            language_names[language]["vacancies_found"] = count_superjob_vacancies(programmer, 4, clue)

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

        jobs = list(filter(lambda x: x is not None, vacancies_processed))
        language_names[language]["vacancies_processed"] = len(jobs)

        average_salery = 0
        for vacanc in jobs:
            average_salery += int(vacanc)
        if len(jobs) == 0:
            language_names[language]["average_salary"] = 0
        else:
            language_names[language]["average_salary"] = round(average_salery / len(jobs))
    return language_names


def show_table_jobs(clue, title):
    table = draw_table(collect_vacancies_from_api(clue))
    table_jobs = AsciiTable(table, title)
    return table.table_jobs


if __name__ == "__main__":
    load_dotenv()
    print(show_table_jobs('items', 'HeadHunter Moscow'))
    print(show_table_jobs('objects', 'SuperJob Moscow'))
