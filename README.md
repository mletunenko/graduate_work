# Проектная работа: диплом

Бизнес захотел дать пользователям возможность создавать свои профили, где можно добавлять понравившиеся фильмы к себе, ставить рейтинг каждому фильму и писать свой отзыв. Вам пришло задание создать систему, которая будет управлять профилями пользователей. В этом сервисе бизнес предлагает сохранять чувствительную информацию о человеке: номер телефона и ФИО. Номер телефона бизнес далее будет использовать в маркетинговых коммуникациях, для определения уникальности пользователя, а также для двухфакторной авторизации.

Что нужно сделать:

- Сделать CRUD работы с профилем пользователя.
- Подключить просмотр профилей клиентов в админке (только тем, у кого есть права
на доступ к таким данным).
- Сделать возможность добавлять понравившиеся фильмы в профиль.
- Сделать возможность выставлять свой собственный рейтинг фильму как в Кинопоиске/IMDB.
- Сделать возможность оставлять рецензии на фильм.
- Добавить к каждому фильму возможность смотреть отзывы пользователей и рейтинг.

# Запуск приложения

## Docker-compose

1. Выполнить команды:
```bash
docker compose up -d
```

## Локальный запуск

1. Активировать venv и создать .env по образцу
2. Установить зависимости

```bash
pip install --upgrade pip && pip install -r requirements.txt
```
3. Используйте docker-compose.yml 

Так же поднятие контейнеров с сервисами для локальной работы доступны через 

```bash
dc up -d profiles_pg
```
(dc up --build profiles_pg profiles_rabbitmq)
4. Используйте Sentry 

login: mletunenko@gmail.com

pass: 8s.mf#2FRbVVRj7

5. Переменные окружения в конфиге по умолчанию для локального запуска.

6. Запуск приложения

```bash
python src/web_server.py 
```
7. Запуск воркера

```bash
python src/worker.py 
```
## Связанные репозитории

Сервис выдачи контента
- https://github.com/mletunenko/Async_API_sprint_1_team

Сервис административной панели 
- https://github.com/mletunenko/new_admin_panel_sprint_3

Сервис авторизации
- https://github.com/mletunenko/Auth_sprint_1

Сервис аналитики пользовательских действий
- https://github.com/mletunenko/ugc_sprint_1

Сервис хранения пользовательского контента
- https://github.com/mletunenko/ugc_sprint_2

Сервис профили (Дипломный проект, текущий репозиторий)
- https://github.com/mletunenko/graduate_work