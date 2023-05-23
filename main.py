import requests
import json
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable
import os


def get_headhunter_vacancies(title, page, city, per_page, timeline):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 (fannyfanny879@gmail.com)',
        'Accept-Language': 'ru-RU'
    }

    params = {
        'text': title,
        'area': city,
        'page': page,
        'per_page': per_page,
        'search_period': timeline
    }

    url = "https://api.hh.ru/vacancies"
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)
    response.raise_for_status()
    return response.json()


def get_superjob_vacancies(title, page, per_page, timeline):
    headers = {
        "X-Api-App-Id": os.environ["SUPER_JOB_SECRET_KEY"],
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        'keywords': title,
        'page': page,
        'count': per_page,
        'period': timeline
    }

    url = "https://api.superjob.ru/2.0/vacancies/"
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)
    response.raise_for_status()
    return response.json()


def count_headhunter_vacancies(job, pages, clue):
    count = 0
    for page in range(pages):
        vacancies = get_headhunter_vacancies(job, page, city=1, per_page=20, timeline=30) 
        count += len(vacancies[clue])
    return count


def count_superjob_vacancies(job, pages, clue):
    count = 0
    for page in range(pages):
        vacancies = get_superjob_vacancies(job, page, per_page=20, timeline=30)
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


def parse_headhunter(job, clue='items'):
    vacancies_processed = []
    vacancies_found = count_headhunter_vacancies(job, 4, clue)
    headhunter_vacancies = get_headhunter_vacancies(job, city=1, page=4, per_page=20, timeline=30)
    for vacancies in headhunter_vacancies[clue]:
        vacancies_salary = vacancies['salary']
        vacancies_processed.append(predict_rub_salary_for_headhunter(vacancies_salary))
    return vacancies_found, vacancies_processed


def parse_superjob(job, clue='objects'):
    vacancies_processed = []
    vacancies_found = count_superjob_vacancies(job, 4, clue)
    superjob_vacancies = get_superjob_vacancies(job, page=4, per_page=20, timeline=30)
    for vacancies in superjob_vacancies[clue]:
        if vacancies['town']['title'] == 'Москва':
            vacancies_processed.append(predict_rub_salary_for_superJob(vacancies))
    return vacancies_found, vacancies_processed


def collect_vacancies_from_api(title):
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
    for language in language_names:
        programmer = "Программист {}".format(language)

        parsers = {
            "HeadHunter": parse_headhunter(programmer),
            "SuperJob": parse_superjob(programmer)
        }

        vacancies_found, vacancies_processed = parsers[title]

        language_names[language]["vacancies_found"] = vacancies_found

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


def show_table_jobs(title):
    table_jobs = draw_table(collect_vacancies_from_api(title))
    table = AsciiTable(table_jobs, "{} Moscow".format(title))
    return table.table


if __name__ == "__main__":
    load_dotenv()
    print(show_table_jobs('HeadHunter'))
    print(show_table_jobs('SuperJob'))
