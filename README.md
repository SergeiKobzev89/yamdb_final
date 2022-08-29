# Групповой проект «Yamdb»
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
- Документация к API доступна по адресу http://127.0.0.1/redoc/

### Установка
##### Шаг 1. Проверьте установлен ли у вас Docker
Прежде, чем приступать к работе, необходимо знать, что Docker установлен. Для этого достаточно ввести:
```sh
docker -v
```
Или скачайте Docker Desktop для Mac или Windows. Docker Compose будет установлен автоматически. В Linux убедитесь, что у вас установлена последняя версия Compose. Также вы можете воспользоваться официальной инструкцией.

##### Шаг 2. Клонируйте репозиторий себе на компьютер
Введите команду:
```sh
git clone https://github.com/DenisSivko/infra_sp2.git
```
##### Шаг 3. Создайте в клонированной директории файл .env
Пример:
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
##### Шаг 4. Запуск docker-compose
Для запуска необходимо выполнить из директории с проектом команду:
```sh
docker-compose up -d
```
##### Шаг 5. База данных
Создаем и применяем миграции:
```sh
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
```
##### Шаг 6. Подгружаем статику
Выполните команду:
```sh
docker-compose exec web python manage.py collectstatic --no-input 
```
##### Шаг 7. Заполнение базы тестовыми данными
Для заполнения базы тестовыми данными вы можете использовать файл fixtures.json, который находится в infra_sp2. Выполните команду:
```sh
docker-compose exec web python manage.py loaddata fixtures.json
```
##### Дополнительные команды
Создание суперпользователя:
```sh
docker-compose exec web python manage.py createsuperuser
```
Остановить работу всех контейнеров можно командой:
```sh
docker-compose down
```
Для пересборки и запуска контейнеров воспользуйтесь командой:
```sh
docker-compose up -d --build 
```
Мониторинг запущенных контейнеров:
```sh
docker stats
```
Останавливаем и удаляем контейнеры, сети, тома и образы:
```sh
docker-compose down -v
```

### Авторы
***Первый разработчик*** (https://github.com/Ermakov-Viktor) - писал всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail.
***Второй разработчик*** (https://github.com/do-217nr) - писал категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.
***Третий разработчик*** (https://github.com/SergeiKobzev89) - занимался отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивал эндпойнты, определял права доступа для запросов. Рейтинги произведений, а также реализация механизма импорта данных из csv файлов, тоже достались третьему разработчику.