# TodoAPI
TodoAPI is an A RESTful api built on Python-Flask framework that allows a user to create, update and delete todos

## Badges
<!---[![Coverage Status](https://coveralls.io/repos/github/OlukaDenis/TodoAPI/badge.svg?branch=develop)](https://coveralls.io/github/OlukaDenis/TodoAPI?branch=develop)
[![Build Status](https://travis-ci.com/OlukaDenis/TodoAPI.svg?branch=master)](https://travis-ci.com/OlukaDenis/TodoAPI)-->


## Features

* User can: 
    1. Create an account and log in
    2. Admin user can promote users to admin
    3. Admin user can view all other users
    4. Admin user can delete users
    5. Can create a todo
    6. Delete a todo
    7. Update a todo as being completed
    8. View all todos

## Endpoints

#### User Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/user` | Create a user
POST | `/admin` | Create a admin user
GET | `/login` | Login a user 
DELETE | `/user/<public_id>` | Delete user

#### Todo Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/todo` | Crteate a todo
GET | `/todo` | Lists all todos
GET | `/todo/<todo_id>` | Retrieve a specific todo
PUT | `/todo/<todo_id>` | Complete a todo
DELETE | `/todo/<todo_id>` | Delete a todo

## Tools Used

* [Flask](http://flask.pocoo.org/) - Framework for Python
* [Virtual environment](https://virtualenv.pypa.io/en/stable/) - Tool used to create isolated python environments
* [pip](https://pip.pypa.io/en/stable/) - Package installer for Python

## Getting Started


* Clone the project into your local repository using this command:

            `git clone https://github.com/OlukaDenis/TodoAPI.git`

* Change directory to the cloned folder using the following command for Windows, Linux and MacOS

            `cd TodoAPI`

* If you do not have a virtual environment installed run the following command, else follow the next steps.

            `pip install virtualenv`
            
* Create a virtual environment(for Windows, Linux and MacOS)

            `virtualenv venv`

* Activate the virtual environment(Windows only)

            `source venv/Scripts/activate`

     and for Linux and MacOS

            `source venv/bin/activate`

* Run the app(for Windows, Linux and MacOS)

            `python api.py`

:wink:
