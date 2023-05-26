import requests
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


def get_superjob_vacancies(title, secret_key, page, city, per_page, timeline):
    headers = {
        "X-Api-App-Id": secret_key,
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


def count_salary(job, salary_from, salary_to):
    if job[salary_from] and job[salary_to]:
        return (job[salary_from] + job[salary_to]) / 2
    elif job[salary_from]:
        return job[salary_from] * 1.2
    else:
        return job[salary_to] * 0.8


def predict_rub_salary_for_headhunter(vacancy):
    if vacancy and vacancy['currency'] == 'RUR':
        salary = count_salary(vacancy, 'from', 'to')
        return salary


def predict_rub_salary_for_superJob(vacancy):
    if vacancy:
        salary = count_salary(vacancy, 'payment_from', 'payment_to')
        return salary


def parse_headhunter(job, secret_key, pages, clue='items'):
    vacancies_salary = []
    vacancies_found = 0
    for page in range(pages):
        headhunter_vacancies = get_headhunter_vacancies(job, city=1, page=page, per_page=100, timeline=30)
        vacancies_found += len(headhunter_vacancies[clue])
        for vacancy in headhunter_vacancies[clue]:
            vacancie_salary = vacancy['salary']
            vacancies_salary.append(predict_rub_salary_for_headhunter(vacancie_salary))
    return vacancies_found, vacancies_salary


def parse_superjob(job, secret_key, pages, clue='objects'):
    vacancies_salary = []
    vacancies_found = 0
    for page in range(pages):
        superjob_vacancies = get_superjob_vacancies(job, secret_key, page=page, city=4, per_page=100, timeline=30)
        vacancies_found += len(superjob_vacancies[clue])
        for vacancy in superjob_vacancies[clue]:
            vacancies_salary.append(predict_rub_salary_for_superJob(vacancy))
    return vacancies_found, vacancies_salary


def get_statistics_from_api(title, secret_key=''):
    job_statistics = {
        # "Python": {},
        # "Java": {},
        # "JavaScript": {},
        # "С++": {},
        # "C#": {},
        # "Ruby": {},
        # "PHP": {},
        # "C": {},
        "Swift": {},
        "Go": {}
    }
    for language in job_statistics:
        programmer = "Программист {}".format(language)

        parsers = {
            "HeadHunter": parse_headhunter,
            "SuperJob": parse_superjob
        }

        parser = parsers[title]
        vacancies_found, vacancies_salary = parser(programmer, secret_key, pages=2)

        job_statistics[language]["vacancies_found"] = vacancies_found

        all_salaries = list(filter(lambda x: x, vacancies_salary))
        job_statistics[language]["vacancies_processed"] = len(all_salaries)

        if len(all_salaries):
            job_statistics[language]["average_salary"] = round(sum(all_salaries) / len(all_salaries))
        else:
            job_statistics[language]["average_salary"] = 0
    return job_statistics


def draw_table(job_statistics):
    table_jobs = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for language, description in job_statistics.items():
        table_jobs.append([language, str(description['vacancies_found']), str(description['vacancies_processed']), str(description['average_salary'])])

    table = AsciiTable(table_jobs, "{} Moscow".format(job_statistics))
    return table.table


if __name__ == "__main__":
    load_dotenv()
    super_job_secret_key = os.environ["SUPER_JOB_SECRET_KEY"]
    headhunter_job_statistics = get_statistics_from_api('HeadHunter')
    superjob_job_statistics = get_statistics_from_api('SuperJob', super_job_secret_key)
    print(draw_table(headhunter_job_statistics))
    print(draw_table(superjob_job_statistics))
