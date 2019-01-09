# drf-demo
A django rest framework demo project along with search feature and unit test consisting JWT authentication.

## Requirements (Tested on)
1. Ubuntu 18.04
2. Python 3
3. django 2.1.2

## How to execute it to run on your local machine.
Note: Activate virtual environment.
1. git clone https://github.com/bickypaul/drf-demo/
2. cd drf-demo
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver
6. Goto http://localhost:8000

## Unit Testing
1. python manage.py test

Testing consists login test, add item in database, get item from database, get a single item from database, post method permissions, JWT authenication test. 
