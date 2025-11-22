from faker import Faker
from typing import List, Dict

fake = Faker(['ru_RU'])
# fake = Faker('en_US')

def generate_russian_users(count: int = 10) -> List[Dict]:
    users = []
    for i in range(count):
        user = {
            'id': i + 1,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.middle_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'city': fake.city(),
            'address': fake.address(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=65),
            'job': fake.job(),
            'company': fake.company()
        }
        users.append(user)
    return users

# Генерация 5 русских пользователей
users = generate_russian_users(5)
for user in users:
    print(f"{user['last_name']} {user['first_name']} {user['middle_name']} - {user['city']}")
