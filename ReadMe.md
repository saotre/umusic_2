# Проект "Аудио хранитель" (umusic)

Веб сервис реализующий API для создания пользователей и сохранения в БД аудио файлов отдельно для каждого пользователя.
Для установки и запуска данного проекта используется docker-окружение.

## Используемые технологии
- _Python 3_
- _FastAPI_
- _Uvicorn_
- _SQLAlchemy_
- _PostgresSQL_
- _Docker_
- _Ffmpeg_

## Как установить
Клонировать репозиторий в целевую папку на машине с установленным ПО Docker.
В терминале зайти в каталог с файлом "docker-compose.yml". Выполнить команду:
```
docker-compose up
```

## Как использовать
После развертывания и запуска docker-контейнеров (контейнеры: app и postgres), можно обращаться к сервису по адресу http://localhost:8000
API cервиса реализует три запроса:
- Запрос на создание пользователя
- Запрос добавление аудиозаписи
- Запрос на скачивание аудиозаписи

Примеры запросов:

1. Запрос на создание пользователя:
   пример:
   request:
      POST http://localhost:8000/user
      body: {"name": "Egor Andreev"}
   response:
      {
         "name": "Egor Andreev",
         "id": "9d9102ca-25bb-4199-abc4-72a6c5db1fc6",
         "token": "2b8f40d5-7073-4591-8ee0-46444fff1ded",
         "created_at": "2023-06-06T16:51:50.603229"
      }

2. Запрос добавление аудиозаписи
   пример:
   request:
      POST http://localhost:8000/audio?user_id=9d9102ca-25bb-4199-abc4-72a6c5db1fc6&token=2b8f40d5-7073-4591-8ee0-46444fff1ded
      body: File: file_example_WAV_1MG.wav (type: "audio/wav"; size: 1073218 bytes)
   response:
      "http://localhost:8000/record?id=36d18862-4a6c-4c68-82e2-ae3d9fd46a38&user=9d9102ca-25bb-4199-abc4-72a6c5db1fc6"

   Если пользователь с такими user_id + token не найден, возвращается ответ с http-статусом 404 "Doesn't exist such user + token"

3. Запрос на скачивание аудиозаписи.
   пример:
   request:
      GET  http://localhost:8000/record?id=36d18862-4a6c-4c68-82e2-ae3d9fd46a38&user=9d9102ca-25bb-4199-abc4-72a6c5db1fc6
   response:
      файл mp3: 36d18862-4a6c-4c68-82e2-ae3d9fd46a38.mp3 (имя файла: id_аудиозаписи.mp3)

   Если аудиозапись с указанным id и для указанного пользователя не найдены возвращается ответ с http-статусом 404 "Audio file is not found"


В каталоге api/wav/ присутствует пример wav-файла (1 Мб) для использования в тестах запросов.



