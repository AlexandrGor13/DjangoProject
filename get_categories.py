import sqlite3
import json

# Подключиться к базе данных SQLite
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

# Выполнить SQL-запрос
cursor.execute("SELECT * FROM shop_app_category")
rows = cursor.fetchall()

# Получить имена столбцов
columns = [column[0] for column in cursor.description]
# Преобразовать строки в JSON
results = [dict(zip(columns, row)) for row in rows]
json_data = json.dumps(results, indent=4, ensure_ascii=False)

# Сохранить данные в файл
with open('category.json', 'w') as json_file:
    json_file.write(json_data)

# Закрыть соединение
connection.close()