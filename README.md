# Финал проекта YaTube(API)

### YaTube - cоциальная сеть для публикации личных дневников №1 в мире*
_* по версии автора_

## Возможности YaTube(API)
- регистрация нового пользователя
- получение и обновление токена
- возможность получения списка постов, групп, коментарией и любимых авторов
- возможность публикации записей с картинками
- возможность подписываться на любимых авторов
- возможность оставлять комментарии 


**Для не авторизованного пользователя возможен только просмотр списка постов, групп и комментариев**

## Технологии

* [Python 3.7](https://www.python.org/downloads/release/python-370/)
* [Django 2.2.19](https://docs.djangoproject.com/en/4.1/)
* [DRF 3.12.4](https://www.django-rest-framework.org/community/release-notes/)

## Установка

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Evgen-mtr/api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserverd
```

## Автор

