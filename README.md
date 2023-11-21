# internship_backend

The internship_backend project is a web application that utilizes Docker and Django for management and deployment.

## Running the Project Using Docker Compose

1. **Cloning the Repository**:

   First, clone the repository using Git:

   ```bash
   git clone https://github.com/krignalion/quiz-wiz-backend.git
   cd ./quiz-wiz-backend
   ```
   
2. **Setting up the Environment**:

   Rename the `.env.sample` file to `.env` in the project root and fill in the environment variables.

4. **Running the Project**:
   ```bash
   docker-compose up --build
   ```
   The application will be accessible at http://localhost:8000.

4. **Stopping the Project**:
   ```bash
   docker-compose down
   ```
   
## Applying and Running Migrations:

1. **Creating Migrations**:
   ```bash
   docker-compose run django_app python manage.py makemigrations
   ```
   
2. **Applying Migrations**:
   ```bash
   docker-compose run django_app python manage.py migrate
   ```
   This command will update the database according to the current migrations.

Acknowledgements

Thank you for your attention to our project!