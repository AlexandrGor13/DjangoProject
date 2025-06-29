## Проект интернет-магазина строительных товаров
#### Проект написан на python 3.12 с использование Django, Celery, Redis, Postgres

Для запуска проекта необходимо клонировать репозиторий следующей командой.

`git clone https://github.com/AlexandrGor13/DjangoProject.git`


Перед запуском следует настроить переменные окружения по имеющемуся шаблону.
`.env.example -> .env`

Для сборки контейнера требуется запустить docker compose.
`docker compose up`
В случае удачного запуска контейнера проект будет запущен.

Для заполнения базы данных сведениями о товарах запустите
`docker compose exec backend uv run python manage.py generate_data`

Для настройки celery запустите следующую команду:
`docker compose exec backend uv run python manage.py create_intervals`

Чтобы перейти на страницу проекта, наберите в браузере http://0.0.0.0:8080

Для запуска панели администратора создайте администратора командой
`docker compose exec backend uv run python manage.py createsuperuser`.

Для входа в панель администратора, наберите в браузере http://0.0.0.0:8080/admin

В проекте можно регистрировать пользователей, просматривать и выбирать товары, создавать заказы, проводить тестовую оплату через ЮKassa.