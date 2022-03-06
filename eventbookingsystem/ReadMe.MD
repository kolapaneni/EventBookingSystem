
Steps to setup the project

1. Clone the project into your local repository
2. Install Docker
3. Navigate to the `eventbookingsystem` directory with `cd eventbookingsystem` from your terminal

Steps to Run the project with Docker
1. To run the project, run the command 
   1. `sudo docker-compose up -d  --build` in your terminal
2. Make migrations with the following command 
   1. `sudo docker-compose exec web python manage.py makemigrations`
3. Migrate the DB schema with the following command 
   1. `sudo docker-compose exec web python manage.py migrate`
4. Create a Super User if needed with the following command 
   1. `sudo docker-compose exec web python manage.py createsuperuser`
5. Run the test cases with the following command
   2. `sudo docker-compose exec web python manage.py test eventbookings.tests`
6. Open a browser and check if the server is up with this URL 
   1. `http://127.0.0.1:8000/admin`. If a page opens up, the server is running successfully.
7. Docker is reading the environmental variables from `dev.env` file.
8. If needed, we can change the environmental variables from `dev.env` file. 


Steps to Run the project without Docker
1. Create a virtual environment
   1. Install pipenv package with the following command
      1. `pip install virtualenv`
   2. Create virtual environment with this command
      1. `virtualenv -p python venv`
   3. Activate virtual environment 
      1. `source venv/bin/activate`
   4. Install required packages
      1. `pip install -r requirements.txt`
2. In `eventbookingsystem/settings.py`, change the DB credentials and DB name
3. Make migrations with the following command 
   1. `python manage.py makemigrations`
4. Migrate the DB schema with the following command 
   1. `python manage.py migrate`
5. Create a Super User if needed with the following command 
   1. `python manage.py createsuperuser`
6. Run server with the following command
   1. `python manage.py runserver`
7. Run the test cases with the following command
   1. `python manage.py test eventbookings.tests`
   