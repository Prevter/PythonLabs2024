import csv, os, datetime
import matplotlib.pyplot as plt

def create_pie_chart(data: dict, title: str):
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    plt.title(title)
    plt.show()

def create_bar_chart(data: list[dict], title: str):
    # each item in data is a separate bar chart with title and data
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(title)
    for i in range(2):
        for j in range(2):
            item = data[i * 2 + j]
            axs[i, j].bar(item['data'].keys(), item['data'].values())
            axs[i, j].set_title(item['title'])
    plt.show()


def count_gender(users: list[dict], gender: str) -> int:
    return sum(1 for user in users if user['Стать'] == gender)

def get_age(birthdate: str) -> int:
    try:
        birthdate = birthdate.split('.')
        birthdate = list(map(int, birthdate))
        birthdate = datetime.date(birthdate[2], birthdate[1], birthdate[0])
    except Exception as e:
        raise ValueError(f'Invalid birthdate format "{birthdate}": {e}')
    
    current_year = datetime.datetime.now().year
    age = current_year - birthdate.year
    if datetime.date(current_year, birthdate.month, birthdate.day) > datetime.datetime.now().date():
        age -= 1
    return age


def split_age_groups(users: list[dict]) -> dict:
    age_groups = {
        'younger_18': [],
        '18-45': [],
        '45-70': [],
        'older_70': []
    }

    for user in users:
        age = get_age(user['Дата народження'])
        if age < 18:
            age_groups['younger_18'].append(user)
        elif age < 45:
            age_groups['18-45'].append(user)
        elif age < 70:
            age_groups['45-70'].append(user)
        else:
            age_groups['older_70'].append(user)
    
    return age_groups

def main():
    if not os.path.exists('users.csv'):
        print('File users.csv not found')
        return
    
    try:
        with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            users = list(reader)
    except Exception as e:
        print(f'Error reading file: {e}')
        return
    
    try:
        males = count_gender(users, 'Male')
        females = count_gender(users, 'Female')
    except Exception as e:
        print(f'Error counting genders: {e}')
        return
    
    try:
        groups = split_age_groups(users)
        gender_groups = [(count_gender(l, 'Male'), count_gender(l, 'Female')) for l in groups.values()]
    except Exception as e:
        print(f'Error grouping users: {e}')
        return
    
    # Part 1
    print(f"Чоловіки: {males}")
    print(f"Жінки: {females}")
    create_pie_chart({ "Чоловіки": males, "Жінки": females }, "Співвідношення статей")
    print()

    # Part 2
    GROUP_NAMES = {
        'younger_18': 'До 18',
        '18-45': '18-45',
        '45-70': '45-70',
        'older_70': 'Від 70'
    }
    print(f"Age groups:")
    for group, users in groups.items():
        print(f"{GROUP_NAMES[group]}: {len(users)}")
    print()
    
    create_pie_chart({ 
        GROUP_NAMES[group]: len(users) for group, users in groups.items() 
    }, "Вікові групи")

    # Part 3
    print("Вікові групи по статям (Чоловіки/Жінки):")
    for i, group in enumerate(gender_groups):
        print(f"{GROUP_NAMES[list(groups.keys())[i]]}: {group[0]}/{group[1]}")
    
    create_bar_chart([{ 
        'title': f"{GROUP_NAMES[list(groups.keys())[i]]}", 
        'data': { 'Чоловіки': group[0], 'Жінки': group[1] }
    } for i, group in enumerate(gender_groups)], "Вікові групи по статям")


if __name__ == '__main__':
    main()