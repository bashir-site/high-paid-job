# HeadHunter и SuperJob check app

HeadHunter и SuperJob check app is a Python script for searching jobs on this platforms. The program find jobs for the most popular programming languages.

## Installation

First of all you need to download all the files in this repo to your computer. Then you need to create and run a virtual environment with these commands:

On Mac OS and Linux:
```bash
# create environment with name venv
virtualenv venv -p python3
# runing venv enviroment
source venv/bin/activate
```

On Windows:
```bash
# create environment with name env
python -m venv env
# runing env enviroment
env\Scripts\activate
```

The next step is to install the necessary modules. This command will help:
```bash
pip install -r requirements.txt
```


## Usage

To run the `main.py` file you need to write this command:

```bash
python main.py 
```
this command conect to headhunter and superjob api's and then create tables with jobs and average salary. The output should be like this:

```bash
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 80               | 2                   | 272500           |
| Java                  | 80               | 1                   | 133000           |
| JavaScript            | 80               | 5                   | 116500           |
| С++                   | 80               | 2                   | 132500           |
| C#                    | 80               | 3                   | 135833           |
| Ruby                  | 80               | 2                   | 197500           |
| PHP                   | 80               | 9                   | 189722           |
| C                     | 80               | 5                   | 156500           |
| Swift                 | 80               | 1                   | 100000           |
| Go                    | 80               | 1                   | 200000           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 80               | 6                   | 76958            |
| Java                  | 13               | 0                   | 0                |
| JavaScript            | 80               | 4                   | 85375            |
| С++                   | 80               | 0                   | 0                |
| C#                    | 80               | 0                   | 0                |
| Ruby                  | 80               | 4                   | 86312            |
| PHP                   | 23               | 0                   | 0                |
| C                     | 80               | 0                   | 0                |
| Swift                 | 1                | 0                   | 0                |
| Go                    | 4                | 0                   | 0                |
+-----------------------+------------------+---------------------+------------------+
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Project Goals
This code was written for educational purposes as part of an online course for web developers at dvmn.org.

## Contacts

You can find my on telegram: https://t.me/bashir_77