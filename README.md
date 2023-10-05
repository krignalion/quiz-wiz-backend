# internship_backend

Проект internship_backend представляет собой веб-приложение, использующее Docker и Django для управления и развертывания.

## Запуск проекта с помощью Docker Compose

1. **Клонирование репозитория**:

   Сначала склонируйте репозиторий с помощью Git:

   ```bash
   git clone https://github.com/krignalion/meduzzen-backend.git
   cd ./meduzzen-backend
   
2. **Настройка окружения**:
   
    Переименуйте файл .env.sample в .env в корне проекта и заполните переменные окружения

4. **Запуск проекта**:
    ```bash
    docker-compose up --build
Приложение будет доступно по адресу http://localhost:8000.

4. **Остановка проекта**:
    ```bash
    docker-compose down
   
## Применение и запуск миграций:
1. **Создание миграций**:
    ```bash
   docker-compose run django_app python manage.py makemigrations
   
2. **Применение миграций**:
    ```bash
   docker-compose run django_app python manage.py migrate
   
Эта команда обновит базу данных в соответствии с текущими миграциями.

Благодарности

Благодарим за внимание к нашему проекту!
 