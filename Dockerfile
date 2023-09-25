# Используем базовый образ Python
FROM python:3.10.12

# Устанавливаем переменную окружения для Python (необязательно, но рекомендуется)
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы с зависимостями и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта
COPY internship_backend /app/

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
