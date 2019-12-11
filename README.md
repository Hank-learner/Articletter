# Articletter

## What is Articletter

> A python3-flask app to publish and read articles
>
> Developed in a virtual environment for python3

### Deployment

#### Requirements

1. python3,pip

2. flask module(pip install flask)

3. mysql(sudo apt-get install mysql-server libmysqlclient-dev)(pip install flask-mysqldb)(pip install Flask-WTF)(pip install passlib)

basic structure of database is given in sqlinit.sql file, donot directly run it , see the contents
and update mysql password in app.py file

requirements.txt contains the packages and modules needed in pi venv, just run the command in your environment

```sh
source /path/to/venvfolder/bin/activate
pip install -r requirements.txt
```

use the following command to run the project:

```sh
flask run
```

### Features

> Developed with bootstrap4
>
> With login system
>
> Publish articles
>
> Articles can be read by everyone without and account
>

### About project
>
> developed in vs code
>
> default formatter: black(vscode extension: DEPRECATED:Black-Python code formatter)
>
> default tab space = 4space length
