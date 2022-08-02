﻿# api_yamdb
api_yamdb

# Описание

Проект представляет собой API для проекта api_yamdb.

Ключевые моменты:

Применены вьюсеты.

Для аутентификации использованы JWT-токены.

У неаутентифицированных пользователей доступ к API только на чтение. 

Аутентифицированным пользователям разрешено изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения.

# Установка

## 1) Склонировать репозиторий
## 2) Создать и активировать виртуальное окружение для проекта

python -m venv venv

source venv/scripts/activate

## 3) Установить зависимости
python pip install -r requirements.txt

## 4) Сделать миграции
python manage.py makemigrations
python manage.py migrate

## 5) Запустить сервер
python manage.py runserver

# Примеры

Для доступа к API необходимо получить токен: 
Нужно выполнить POST-запрос localhost:8000/api/v1/auth/signup/ передав поля username и email.
API отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на  
эндпоинт /api/v1/auth/token/,в ответе на запрос ему приходит token (JWT-токен).

После регистрации и получения токена пользователь может отправить PATCH-запрос 
на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле.

Затем, отправляя токен с каждым запросом, можно будет обращаться к методам, например: 

/api/v1/titles/ (GET, POST, PATCH, DELETE)
/api/v1/genre/ (GET, POST, DELETE)
/api/v1/categories/ (GET, POST, DELETE)

При отправке запроса необходимо передать токен в заголовке Authorization: Bearer <токен>