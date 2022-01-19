# articles_project

Для запуска проекта установите python версии 3.7 и выше и pip

После клонирования перейдите в склонированную папку и выполните следующие команды:

Создайте виртуальное окружение командой
```bash
python -m venv venv
```

Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
venv\Scripts\activate
```

Установите зависимости командой

```bash
pip install -r requirements.txt
```


Перейдите в папку sourse:
```bash
cd sourse
```

Создайте в директории с проектом файл .env и заполните по примеру

MYSQL_DATABASE=db_name
MYSQL_USERNAME=username
MYSQL_HOST=host
MYSQL_PORT=port
MYSQL_PASSWORD=password

Примените миграции командой
```bash
./manage.py migrate
```

Загрузите фикстурные статьи командой
```bash
./manage.py loaddata dump.json
```

Чтобы запустить сервер выполните:

```bash
./manage.py runserver
```

Для доступа в панель администратора перейдите по ссылке http://localhost:8000/admin
