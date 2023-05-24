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
    print(len(response.json()['items']))
    return response.json()


def get_superjob_vacancies(title, page, city, per_page, timeline):
    headers = {
        "X-Api-App-Id": os.environ["SUPER_JOB_SECRET_KEY"],
        "Authorization": "Bearer r.000000010000001.example.access_token",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        'keywords': title,
        'town': city,
        'page': page,
        'count': per_page,
        'period': timeline
    }

    url = "https://api.superjob.ru/2.0/vacancies/"
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_for_headhunter(vacancie):
    if vacancie:
        if vacancie['currency'] != 'RUR':
            return
        if vacancie['from'] and vacancie['to']:
            return (vacancie['from'] + vacancie['to']) / 2
        elif vacancie['from']:
            return vacancie['from'] * 1.2
        else:
            return vacancie['to'] * 0.8


def predict_rub_salary_for_superJob(job):
    if job['payment_from']:
        if job['payment_from'] + job['payment_to']:
            return round((job['payment_from'] + job['payment_to'])/2)
        elif job['payment_from']:
            return job['payment_from'] * 1.2
        else:
            return job['payment_to'] * 0.8


def parse_headhunter(job, pages, clue='items'):
    vacancies_processed = []
    vacancies_found = 0
    for page in range(pages):
        headhunter_vacancies = get_headhunter_vacancies(job, city=1, page=page, per_page=20, timeline=30)
        vacancies_found += len(headhunter_vacancies[clue])
        for vacancie in headhunter_vacancies[clue]:
            vacancies_salary = vacancie['salary']
            vacancies_processed.append(predict_rub_salary_for_headhunter(vacancies_salary))
    return vacancies_found, vacancies_processed


def parse_superjob(job, pages, clue='objects'):
    vacancies_processed = []
    vacancies_found = 0
    for page in range(pages):
        superjob_vacancies = get_superjob_vacancies(job, page=page, city=4, per_page=20, timeline=30)
        vacancies_found += len(superjob_vacancies[clue])
        for vacancies_number, vacancie in enumerate(superjob_vacancies[clue]):
            vacancies_processed.append(predict_rub_salary_for_superJob(vacancie))
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
            "HeadHunter": parse_headhunter(programmer, pages=4),
            "SuperJob": parse_superjob(programmer, pages=4)
        }

        vacancies_found, vacancies_processed = parsers[title]

        language_names[language]["vacancies_found"] = vacancies_found

        jobs = list(filter(lambda x: x, vacancies_processed))
        language_names[language]["vacancies_processed"] = len(jobs)

        average_salary = 0
        for job_salary in jobs:
            average_salary += int(job_salary)
        if len(jobs):
            language_names[language]["average_salary"] = round(average_salary / len(jobs))
        else:
            language_names[language]["average_salary"] = 0
    return language_names


def draw_table(title):
    language_name = collect_vacancies_from_api(title)

    table_jobs = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for language, description in language_name.items():
        table_jobs.append([language, str(description['vacancies_found']), str(description['vacancies_processed']), str(description['average_salary'])])
    
    table = AsciiTable(table_jobs, "{} Moscow".format(title))
    return table.table


if __name__ == "__main__":
    load_dotenv()
    print(draw_table('HeadHunter'))
    print(draw_table('SuperJob'))
