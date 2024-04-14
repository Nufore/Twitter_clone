# Инструкция по запуску приложения

1. В папку `app` добавить файл `.env` со следующими параметрами
```
DB_HOST=postgres
DB_PORT=5432
DB_NAME=t_clone_db
DB_USER=admin
DB_PASS=admin
```

2. Далее из корневой папки проекта `python_advanced_diploma` выполнить команду `docker compose up --build`
___
# Документация

После запуска приложения документация в виде swagger доступна по [ссылке](http://localhost:8000/docs)
___

# Работа с БД

1. В терминале выполняем команду `docker exec -it db /bin/sh`
2. Затем подключаемся к БД по команде `psql -d t_clone_db -U admin`
3. Проверить список пользователей `select * from users;`
4. Для добавления пользователя используем скрипт
```sql
insert into users
(name, api_key)
values
('test_3', 'test_3');
```
---

# Работа с сайтом
Чтобы открыть страницу сайта, перейдите по [ссылке](http://localhost/)
___

# Тестирование

1. Перейти в директорию `postgres_database`
2. В терминале выполнить команду `docker compose up --build`
3. Из корневой папки в терминале выполнить команду `pytest -v tests/`