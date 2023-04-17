## Overview:
- dj is the devSearch project
- projects folder is a project appa and its respective urls, templates and models
- users folders is a user app its respective urls, templates and models

## Set up project

#### Clone the project 
`` git clone https://github.com/pi2labs/DevSearch.git``

#### Migrate SQL Lite DB:
`` python manage.py migrate``

#### Run server:

``python manage.py runserver 9000`` to port 9000

#### To access admin panel:
``http://127.0.0.1:9000/admin``

#### To create superuser:

``python manage.py createsuperuser`` and follow the instructions to create superuser and login to the admin panel from the above link

#### To access devsearch application:

``http://127.0.0.1:9000/`` this will take to the homepage landing page with list of developers present if added to the database.

## Features in the app:

- Sign-up functionality
- After sign-up you get an email in your inbox
- Forgot password functionality
- Login / logout functionality
- My Account: 
    - Add / delete projects
    - Add / delete skills
    
- When navigating to a new developer from the Developers link in navbar (need to create another account)
- send messages to the developer and chat with him
- Messages will be received in the Inbox
- See projects from other developers.
- REST API's are also available, created a dummy application called Frontend which will send up or down votes to a developer project. 

## Coming up:
- Adding the project to docker, creating new images
- Adding project to AWS, create new DB in RDS
- Adding images to S3 bucket.
- Add project to heroku server.