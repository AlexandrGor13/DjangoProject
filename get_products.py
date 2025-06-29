import json
from decimal import Decimal

import psycopg2
from environs import Env

env = Env()
env.read_env()

connection = psycopg2.connect(
    dbname=env("POSTGRES_DB"),
    user=env("POSTGRES_USER"),
    password=env("POSTGRES_PASSWORD"),
    host=env("POSTGRES_HOST"),
)
cursor = connection.cursor()

cursor.execute("SELECT * FROM app_shop_product")
rows = cursor.fetchall()

columns = [column[0] for column in cursor.description]

results = [dict(zip(columns, row)) for row in rows]
new_result = []
for row in results:
    new_row = {}
    for key, value in row.items():
        if type(value) == Decimal:
            value = str(value)
        new_row[key] = value
    new_result.append(new_row)
json_data = json.dumps(new_result, indent=4, ensure_ascii=False)

with open("products.json", "w") as json_file:
    json_file.write(json_data)

connection.close()
