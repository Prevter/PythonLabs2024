import csv, os, datetime
import xlsxwriter

def get_age(birthdate: str) -> int:
    try:
        birthdate = birthdate.split('.')
        birthdate = list(map(int, birthdate))
        birthdate = datetime.date(birthdate[2], birthdate[1], birthdate[0])
    except Exception as e:
        raise ValueError(f'Invalid birthdate format: {e}')
    
    current_year = datetime.datetime.now().year
    age = current_year - birthdate.year
    if datetime.date(current_year, birthdate.month, birthdate.day) > datetime.datetime.now().date():
        age -= 1
    return age


def compact_user(user: dict) -> dict:
    return {
        'Прізвище': user['Прізвище'],
        'Ім\'я': user['Ім\'я'],
        'По-батькові': user['По-батькові'],
        'Дата народження': user['Дата народження'],
        'Вік': get_age(user['Дата народження']),
    }

def main():
    if not os.path.exists('users.csv'):
        print('File users.csv not found')
        return
    
    try:
        with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            users = list(reader)
            users = [compact_user(user) for user in users]
    except Exception as e:
        print(f'Error reading file: {e}')
        return
    
    age_groups = {
        'all': [],
        'younger_18': [],
        '18-45': [],
        '45-70': [],
        'older_70': []
    }

    try:
        for user in users:
            age = user['Вік']
            age_groups['all'].append({'#': len(age_groups['all']) + 1, **user})
            if age < 18:
                age_groups['younger_18'].append({'#': len(age_groups['younger_18']) + 1, **user})
            elif age < 45:
                age_groups['18-45'].append({'#': len(age_groups['18-45']) + 1, **user})
            elif age < 70:
                age_groups['45-70'].append({'#': len(age_groups['45-70']) + 1, **user})
            else:
                age_groups['older_70'].append({'#': len(age_groups['older_70']) + 1, **user})
    except Exception as e:
        print(f'Error grouping users: {e}')
        return
    
    try:
        workbook = xlsxwriter.Workbook('users.xlsx')
        for group_name, group in age_groups.items():
            worksheet = workbook.add_worksheet(group_name)
            fieldnames = list(group[0].keys())
            for i, fieldname in enumerate(fieldnames):
                worksheet.write(0, i, fieldname)
            for i, user in enumerate(group, 1):
                for j, fieldname in enumerate(fieldnames):
                    worksheet.write(i, j, user[fieldname])

        workbook.close()
    except Exception as e:
        print(f'Error writing to file: {e}')
        return
    
    print('Ok')


if __name__ == '__main__':
    main()