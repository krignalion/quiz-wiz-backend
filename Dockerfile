# Use the Python base image
FROM python:3.11

# Set an environment variable for Python (optional, but recommended)
ENV PYTHONUNBUFFERED 1

# Set an environment variable for Django
ENV DJANGO_SETTINGS_MODULE=internship_backend.settings

# Set the working directory inside the container
WORKDIR /app

# Copy files with dependencies and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory (where the Dockerfile is located) to /app inside the container
COPY . /app/

# Open the port on which the application will run
EXPOSE 8000

# Command to run tests (pytest)
#CMD ["pytest"]

# Create static files
#RUN python manage.py collectstatic --noinput

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
