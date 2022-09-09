![Build Status](https://github.com/SergeiKobzev89/yamdb_final/workflows/yamdb_workflow/badge.svg)


# Групповой проект «Yamdb»

Проект развернут [по адресу:](http://51.250.86.82/api/v1/)


### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок высчитывается средняя оценка произведения.

### Доступные функции
##### REVIEWS
- Получить список всех отзывов
- Создать новый отзыв
- Получить отзыв по id
- Частично обновить отзыв по id
- Удалить отзыв по id

##### COMMENTS
- Получить список всех комментариев к отзыву по id
- Создать новый комментарий для отзыва
- Получить комментарий для отзыва по id
- Частично обновить комментарий к отзыву по id
- Удалить комментарий к отзыву по id

##### AUTH
- Отправление confirmation_code на переданный email
- Получение JWT-токена в обмен на email и confirmation_code

##### USERS
- Получить список всех пользователей
- Создание пользователя
- Получить пользователя по username
- Изменить данные пользователя по username
- Удалить пользователя по username
- Получить данные своей учетной записи
- Изменить данные своей учетной записи

##### CATEGORIES
- Получить список всех категорий
- Создать категорию
- Удалить категорию

##### GENRES
- Получить список всех жанров
- Создать жанр
- Удалить жанр

##### TITLES
- Получить список всех объектов
- Создать произведение для отзывов
- Информация об объекте
- Обновить информацию об объекте
- Удалить произведение

### Workflow
- tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
- build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
- deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
- send_message - Отправка уведомления в Telegram

### Как запустить проект:

Все описанное ниже относится к ОС Linux. Клонируем репозиторий и и переходим в него:

```
git clone git@github.com:SergeiKobzev89/yamdb_final.git
cd yamdb_final 
cd api_yamdb
```

Создаем и активируем виртуальное окружение:

```
python3 -m venv venv 
source /venv/bin/activate (source /venv/Scripts/activate - для Windows) 
python -m pip install --upgrade pip
```

Ставим зависимости из requirements.txt:

```pip install -r requirements.txt```

Переходим в папку с файлом docker-compose.yaml:

```cd infra```

Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):

```docker-compose up -d --build```

Выполняем миграции:

```
docker-compose exec web python manage.py makemigrations reviews 
docker-compose exec web python manage.py migrate --run-syncdb
```

Создаем суперпользователя:

```docker-compose exec web python manage.py createsuperuser```

Србираем статику:

```docker-compose exec web python manage.py collectstatic --no-input```

Для заполнения базы данных:

```python manage.py loaddata fixtures.json```

Останавливаем контейнеры:

```docker-compose down -v``` 

Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432
```

### Авторы
***Первый разработчик*** (https://github.com/Ermakov-Viktor) - писал всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail.
***Второй разработчик*** (https://github.com/do-217nr) - писал категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.
***Третий разработчик*** (https://github.com/SergeiKobzev89) - занимался отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивал эндпойнты, определял права доступа для запросов. Рейтинги произведений, а также реализация механизма импорта данных из csv файлов, тоже достались третьему разработчику.
