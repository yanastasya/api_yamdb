
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

# API для базы данных отзывов YamDB.
Груповой проект в рамках учебного курса Backend Python-разработчик от Яндекс.Практикум.
Создание API по технической документации на Python в фреймфорке Django, командная работа с GitHub.


# Описание
API позволяет создавать и регистрировать пользователей, получать и создавать отзывы, комментарии.

Пользователь с ролью администратора может добавлять новые произведения, категории, жанры, а также редактировать и удалять пользователей, произведения, категории, жанры, отзывы, комментарии.

Пользователь с ролью модератора может редактировать и удалять отзывы и комментарии.

Полную документацию API можно посмотреть после запуска сервера по адресу http://127.0.0.1/redoc.

# Возможности API
## Пользователи/User:

- Получить список всех пользователей
- Получить пользователя по username
- Cоздание пользователя
- Получить данные своей учетной записи
- Отредактировать данные своей учетной записи
- Отредактировать данные пользователя по username (только admin)
- Удалить пользователя по username (только admin)

## Произведения/Title:

### Получить список всех объектов
- Получить информацию о произведении
- Добавить произведение (только admin)
- Отредактировать информацию о произведении (только admin)
- Удалить произведение (только admin)


## Отзывы/Review:

### Получить список всех отзывов
- Получить отзыв по id
- Создать новый отзыв
- Отредактировать отзыв по id (могут admin, moderator и автор отзыва)
- Удалить отзыв по id (могут admin, moderator и автор отзыва)

## Комментарии к отзывам/Comment:

### Получить список всех комментариев к отзыву по id
- Получить комментарий для отзыва по id
- Создать новый комментарий для отзыва
- Отредактировать комментарий к отзыву по id (могут admin, moderator и автор коммента)
- Удалить комментарий к отзыву по id (могут admin, moderator и автор коммента)

## JWT-токен:

### Отправление confirmation_code на переданный email
- Получение JWT-токена в обмен на username и confirmation_code

## Категории произведений/Category:

### Получить список всех категорий
- Cоздать категорию (только admin)
- Удалить категорию (только admin)

## Жанры/Genre:

### Получить список всех жанров
- Создать жанр (только admin)
- Удалить жанр (только admin)

# Технологии
Python, Django, Django Rest Framework, PyJWT, django-filter.

# Алгоритм регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен). В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.

# Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладает правами администратора (admin). Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

# Создание пользователя администратором
- Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая есть в документации).
- При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения.
- После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.
- Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.

# Примеры запросов
Доступно для всех юзеров:

- GET http://127.0.0.7/api/v1/categories/ - вернет список категорий. Можно использовать поиск по названию категории, добавив ?search=name.

- GET http://127.0.0.7/api/v1/genres/ - вернет список жанров. Можно использовать поиск по названию жанра, добавив ?search=name.

- GET http://127.0.0.7/api/v1/titles/ - вернет список произведений. Если затем указать <title_id>, можно вывести одно произведение.

Юзер с правами администратора может отправять запросы POST по этим же url следующего вида:

- для titles: { "name": "string", "year": 0, "description": "string", "genre": [ "string" ], "category": "string" }
- для categories и genres: { "name": "string", "slug": "string" }

Обычному юзеру доступны для GET и POST разделов reviews и comments:

- http://127.0.0.7/api/v1/titles/<title_id>/reviews/
- http://127.0.0.7/api/v1/titles/<title_id>/reviews/<review_id>/comments/

Автор может редактировать и удалять свои отзывы и комменты через PATCH и DELETE запросы по id отзыва или коммента:
- http://127.0.0.7/api/v1/titles/<title_id>/reviews/<review_id>/
- http://127.0.0.7/api/v1/titles/<title_id>/reviews/<review_id>/comments/<comment_id>/

Юзер с правами модератора или админа может редактировать и удалять отзывы других пользователей.

# Как запустить
На локальном компьютере должен быть установлен Python версии 3 или выше.

- Склонировать данный репозиторий на свой локальный компьютер.
- Установить виртуальное окружение:
``` python3 -3.7 -m venv venv ```
- Обновить менеджер pip и установить зависимости:
``` py -m pip install --upgrade pip ```
``` pip install -r requirements.txt. ```
- Выполнить миграции:
``` python manage.py migrate ```

- Далее можно загрузить данные из .csv таблиц командами:
 ``` python manage.py load_category_data ```
 ``` python manage.py load_genre_data ```
 ``` python manage.py load_users_data ```
 ``` python manage.py load_title_data ```
 ``` python manage.py load_genre_title_data ```
 ``` python manage.py load_rewiews_data ```
 ``` python manage.py load_comments_data ```

Запустить локальный сервер:
``` python manage.py runserver ```


Если на вашем ПК установлен Docker, вы можете развернуть этот проект без установки зависимостей на свой ПК. Необхдимая для этого инфраструктура и инструкции находятся в [этом репозитории](https://github.com/yanastasya/infra_sp2/)

# Авторы

[Евгений](https://github.com/Evgen-mtr) - управление пользователями, система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.

[Анастасия Клинцова](https://github.com/yanastasya)  - организация работы в Git, модели, view и эндпоинты для категорий, жанров, произведений, импорт из csv в db, фильтры.

[Саид] - модели, view и эндпоинты для отзывов и комментариев, вывод рейтинга для произведений.
