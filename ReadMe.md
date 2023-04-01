# AnalyserMicroservice
## Required Packages:
- View [requirements.txt](https://github.com/RPOpenSoft2023/AnalyserMicroservice/blob/main/requirements.txt)

## Instructions to build & install the software:
- Clone the repository

  ```
  git clone https://github.com/RPOpenSoft2023/AnalyserMicroservice.git
  ```
- Install Python 3.10 from source

  ```
  https://www.python.org/downloads/release/python-3109/
  ```
- Install virtualenv

  ```
  pip install virtualenv
  ```
- Create virtual environment

  ```
  python -m virtualenv myenv
  ```
- Activate the virtual environment
  Windows:
  
  ```
  ./myenv/Scripts/activate
  ```
  Linux:
  
  ```
  source myenv/bin/activate
  ```
- Add environment variables for connecting to Postgres Database and Users Microservice token verification
  
  Windows:
  
  ```
  [System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
  [System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
  [System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'analyser-db')
  [System.Environment]::SetEnvironmentVariable('USER_MICROSERVICE', 'http://localhost:8000/user/api/')
  [System.Environment]::SetEnvironmentVariable('BANKING_MICROSERVICE', 'http://localhost:8001/banking/api/')

  ```
  Linux:
  
  ```
  export DATABASE_USER='postgres'
  export DATABASE_PASSWORD='demo'
  export DATABASE_NAME='analyser-db'
  export USER_MICROSERVICE='http://localhost:8000/user/api'
  export BANKING_MICROSERVICE='http://localhost:8001/banking/api/'
  ```
- Change directory to the cloned folder i.e. analyserModule

  ```
  cd AnalyserMicroservice/analyserModule
  ```
- Install all the required packages

  ```
  pip install -r ../requirements.txt
  ```
- Make migrations

  ```
  python manage.py makemigrations
  ```
- Migrate to create the tables inside the database

  ```
  python manage.py migrate
  ```
- Create superuser to use django admin panel

  ```
  python manage.py createsuperuser
  ```
  
## Instructions to run the software:
- Run the server

  ```
  python manage.py runserver 8002
  ```
- To access the django admin panel use following url

  ```
  localhost:8002/admin
  ```
