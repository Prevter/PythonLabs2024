from faker import Faker
from transliterate import translit
from typing import Literal
from datetime import datetime
import random, csv, os

faker = Faker(locale='uk_UA')
def gender_pick(gender: Literal['Male', 'Female'], func_name: str) -> str:
    func = getattr(faker, f"{func_name}_{gender.lower()}")
    return func()

def transliterate(cyrillic: str) -> str:
    return translit(cyrillic, 'ru', reversed=True).replace('\'', '').replace('`', '').replace('ʼ', '')

def gen_email(first_name: str, last_name: str) -> str:
    fake_email = faker.email()
    fake_email = fake_email.split('@')
    first_name = transliterate(first_name).lower()
    last_name = transliterate(last_name).lower()
    choices = [first_name, last_name]
    random.shuffle(choices)
    fake_email[0] = ".".join(choices)
    return '@'.join(fake_email)

def pick_gender() -> Literal['Male', 'Female']:
    return random.choices(['Male', 'Female'], weights=[6, 4])[0]

def pick_date(min_year: int, max_year: int) -> str:
    birth_year = random.randint(min_year, max_year)
    fake_date = faker.date_of_birth()
    if fake_date.month == 2 and fake_date.day == 29:
        fake_date = datetime(birth_year, 2, 28) # No leap years
    return f"{fake_date.day:02d}.{fake_date.month:02d}.{birth_year}"

def gen_user():
    gender = pick_gender()
    last_name = faker.last_name()
    first_name = gender_pick(gender, 'first_name')
    middle_name = gender_pick(gender, 'middle_name')
    birthdate = pick_date(1938, 2008)
    occupation = faker.job()
    phone = faker.phone_number()
    city = faker.city()
    address = faker.address()
    email = gen_email(first_name, last_name)
    return {
        'Прізвище': last_name,
        'Ім\'я': first_name,
        'По-батькові': middle_name,
        'Стать': gender,
        'Дата народження': birthdate,
        'Посада': occupation,
        'Місто проживання': city,
        'Адреса проживання': address,
        'Телефон': phone,
        'Email': email,
    }


def main():
    users = [gen_user() for _ in range(2000)]
    with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            '#', 'Прізвище', "Ім'я", 'По-батькові', 
            'Стать', 'Дата народження', 'Посада', 
            'Місто проживання', 'Адреса проживання', 
            'Телефон', 'Email'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, user in enumerate(users, 1):
            writer.writerow({'#': i, **user})

if __name__ == '__main__':
    main()