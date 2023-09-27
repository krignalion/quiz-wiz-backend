1. Download code from github
2. create an environment in the desired folder
  python3 -m venv env
3. activate
  source env/bin/activate
4. install dependencies 
  pip install -r requirements.txt
6. rename the ".env.sample" file to ".env" and specify your parameters
7. Starting the Server: Start the Django web server.
  python manage.py runserver
8. Your application is now running and accessible at http://localhost:8000

#Running with docker

1. git clone https://github.com/krignalion/meduzzen-backend.git
2. cd ./meduzzen-backend 
3. In the Dockerfile you need to select one of two lines (comment out the second)
CMD ["pytest"] (tests will be run) or
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] ( the server will be started)
4. sudo docker build -t <name> .
5. sudo docker run -p 8000:8000 <name>

