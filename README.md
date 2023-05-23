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
| Python                | 80               | 42                  | 223214           |
| Java                  | 80               | 44                  | 248864           |
| JavaScript            | 80               | 46                  | 129174           |
| С++                   | 80               | 47                  | 196138           |
| C#                    | 80               | 44                  | 200366           |
| Ruby                  | 80               | 20                  | 229150           |
| PHP                   | 80               | 66                  | 178535           |
| C                     | 80               | 59                  | 183263           |
| Swift                 | 80               | 32                  | 221719           |
| Go                    | 80               | 35                  | 267200           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 60               | 38                  | 92086            |
| Java                  | 7                | 4                   | 87500            |
| JavaScript            | 69               | 50                  | 74406            |
| С++                   | 73               | 54                  | 85982            |
| C#                    | 7                | 5                   | 85500            |
| Ruby                  | 80               | 55                  | 81128            |
| PHP                   | 10               | 9                   | 102033           |
| C                     | 11               | 10                  | 115750           |
| Swift                 | 1                | 0                   | 0                |
| Go                    | 2                | 1                   | 300000           |
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