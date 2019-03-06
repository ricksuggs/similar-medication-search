### Overview

This project was created with Python3.7 and NodeJS 10.6.0 and has not been tested with other versions.

You can find documentation for installing the correct distribution for your operating system here:
* https://www.python.org/
* https://nodejs.org/

You will also need to install the Python developer libraries for your system:
    
    apt-get install python-dev

### Back end

The back end is a python flask application, using sqlite as a database.

All commands should be run from the 'back-end' directory.

Optional: create a python virtual environment: 

    python -m venv .venv

This will keep this project's python environment separate from
the global python environment

More information here: https://docs.python.org/3/library/venv.html

Activate the environment: 
        
    Posix: source .venv/bin/activate
    Windows: .venv\Scripts\activate.bat

Install the dependencies:

    pip3 install -r requirements.txt
    pip3 install -r requirements-dev.txt

Build the python dev environment:

	python setup.py develop

Run the flask api:

	python start.py

Run the unit tests:

	pytest --cov=api

### Front end

The front end is a React application.

All commands should be run from the 'front-end' directory.

Install the dependencies:

    npm install

Start the app:

    npm start

Run the unit tests:

    npm test -- --coverage
