# Запуск проекта
1. установить зависимости `pip install -R requirements.txt`
2. определить переменную окружения FLASK_APP со значением app `export FLASK_APP=app`
3. Запустить приложение `flask run`

# Инициализация базы данных
удалить файл identifier.sqlite (если он существует) и выполнить `python db_init.py`