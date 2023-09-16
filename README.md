# praktikum_new_diplom

# Проект "Foodgram"

## Описание

**Foodgram** - это онлайн-сервис, который помогает пользователям находить, создавать и делиться рецептами своих любимых блюд. С этим приложением вы сможете легко организовать свою кулинарную коллекцию, находить вдохновение для приготовления новых блюд, и даже делиться своими кулинарными достижениями с другими пользователями.

## Основные функции

### 1. Рецепты

- **Добавление рецептов**: Пользователи могут создавать свои собственные рецепты, добавлять изображения и подробные инструкции по приготовлению.

- **Поиск рецептов**: Сервис предоставляет мощный поиск, который позволяет пользователям находить рецепты по различным критериям, таким как ингредиенты, кухня, категория и другие.

### 2. Список покупок

- **Создание списка покупок**: Пользователи могут добавлять ингредиенты из рецептов в свой список покупок, чтобы легко организовать покупки продуктов.

### 3. Подписка и лента

- **Подписка на пользователей**: Пользователи могут подписываться на других пользователей и следить за их обновлениями, включая новые рецепты.

- **Лента активности**: Пользователи видят обновления от пользователей, на которых они подписаны, в своей персональной ленте.

### 4. Аутентификация и авторизация

- **Регистрация и вход**: Пользователи могут создавать аккаунты, входить в систему и сохранять свои настройки.

- **Авторизация**: Только авторизованные пользователи могут создавать и редактировать рецепты, а также оставлять комментарии.

## Стек используемых технологий

Проект Foodgram разработан с использованием современных технологий веб-разработки, включая:

- **Django**: Python-фреймворк для создания веб-приложений.

- **Django REST framework**: Библиотека для создания RESTful API.

- **HTML/CSS/JavaScript**: Для создания пользовательского интерфейса и взаимодействия с клиентами.

- **Docker**: Для контейнеризации и упрощения развертывания приложения.

- **Python**: Высокоуровневый, интерпретируемый и общего назначения язык программирования. С применением данного языка написан проект.

- **Gunicorn**: WSGI (Web Server Gateway Interface) HTTP-сервер для приложений Python.

- **NGINX**: Высокопроизводительный веб-сервер, прокси-сервер и сервер обработки обратного прокси, а также сервер для раздачи статических файлов.

- **PostgreSQL**: Мощная, открытая реляционная система управления базами данных (RDBMS).

Проект доступен по адресу: https://fooddisp.bounceme.net/recipes

## Порядок установки

#### Развернуть проект на удаленном сервере:

* Клонировать репозиторий:

```
git@github.com:meveladron/foodgram-project-react.git
```

* Установить на сервере Docker, Docker Compose:

```
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

Создать папку foodgram и перейти в неё

```
mkdir foodgram
cd foodgram
```

* Перенести на сервер 3 файла и перенести в них содержимое:

```
sudo nano .env
sudo nano nginx.conf
sudo nano docker-compose.yml
```

* Для работы с github actions, добавьте секреты.

```
SECRET_KEY              # Secret key проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # username Docker Hub
HOST                    # IP адрес удалённого сервера
USER                    # имя пользователя удалённого сервера
PASSPHRASE              # Пароль удалённого сервера
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # По умолчанию postgres
POSTGRES_USER           # По умолчанию postgres
POSTGRES_PASSWORD       # По умолчанию postgres
DB_HOST                 # По умолчанию db
DB_PORT                 # По умолчанию 5432
```

* Поднять docker-compose:
```
docker-compose up -d --build
```

* Выполнить миграции, создать суперпользователя, собрать статику, Наполнить Базу Данных ингредиентами:

```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py import_recipes
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --noinput
```