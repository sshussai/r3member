# R3MEMBER - A Django web app for quick tips and tricks

Using Django, MySQL and Bootstrap, along with other technologies, this webapp allows users to post shortcuts, tips and 
and tricks they've learned. Ideally, this app will not contain fully detailed, thorough tutorials, but quick tips, along
with an example if possible, to do something.

This app is deployed at: http://162.246.157.122/

## Getting Started

### Prerequisites

This application uses the following Python dependencies:
* Python 3.6.*
* Django 2.1.4
* mysqlclient 1.3.13
* django-crispy-forms 1.7.2
* Pillow 5.4.1
* **gunicorn 19.9.0

** gunicorn is used for deployment

Also, to send emails from Django, this app uses a gmail account, with an app password. To generate an app password for a gmail account, refer to [this article on Google](https://support.google.com/accounts/answer/185833?hl=en)


### Installing

If you would like to clone this project:

* Create a venv running Python 3.6.* and activate it
```
$ python3.6 -m venv "r3member_env"
$ source r3member_env/bin/activate

```
* Clone the repo using the command
```
$ git clone https://github.com/sshussai/r3member.git
```
* Install the required Python packages using the requirements.txt file
```
$ pip install -r requirements.txt
```
* Create file called "dev_vars.txt" that contains the security settings needed by the app. The file must be in the following format, along with the keys
```
example:
{
    "EMAIL_HOST_USER": "<gmail address you would like Django to send emails from>",
    "EMAIL_HOST_PASSWORD": "<gmail key>",
    "SECRET_KEY":"<secret key>"
}
```
* Switch to the dev branch 
```
$ git checkout dev
```
* Make the migrations files and migrate the tables
```
$ python manage.py makemigrations
$ python manage.py migrate

```
* Create a user that you can use to login
```
$ python manage.py createsuperuser <username>
```
* Run the dev server
```
$ python manage.py runserver
```

## Deployment

The following guide can be used to deploy this application on Linux (Ubuntu) server, using Nginx and gunicorn:

### To configure the project:

* Create a venv running Python 3.6.* and activate it
```
$ python3.6 -m venv "r3member_env"
$ source r3member_env/bin/activate

```
* Clone the repo using the command
```
$ git clone https://github.com/sshussai/r3member.git
```
* Install the required Python packages using the requirements.txt file
```
$ pip install -r requirements.txt
```
* Create a MySQL database, accessible by the Django server, along with an appropriate user. 
```
example:
$ mysql -u root -p

mysql> CREATE DATABASE <database_name>
mysql> GRANT ALL PRIVILEGES ON <database_name>.* TO '<database_user>'@'localhost' IDENTIFIED BY '<database_password>';

```
* Create file called "vars.txt" that contains the security settings needed by the app. The file must be in the following format, along with the keys
```
example:
{
    "EMAIL_HOST_USER": "gmail_address",
    "EMAIL_HOST_PASSWORD": "gmail_app_password",
    "DB_ENGINE":"django_backend_for_database",
    "DB_NAME":"database_name",
    "DB_USER":"database_username",
    "DB_PASSWORD":"database_password",
    "DB_HOST":"database_host",
    "DB_PORT":"database_port",
    "SECRET_KEY":"secret_key"
}
```
* Create the migration files and migrate the tables
```
$ python manage.py makemigrations
$ python manage.py migrate 
```
* Create a user to log in to the application
```
$ python manage.py createsuperuser
```


### To configure Nginx and gunicorn
* Create a file called "gunicorn.service" in the "/etc/systemd/system/" folder, in the following format:
```
filename: /etc/systemd/system/gunicorn.service
----

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=<username>
Group=www-data
WorkingDirectory=/<path_to_django_project_folder>
ExecStart=/<path_to_project_virtual_environment>/bin/gunicorn --access-logfile - --workers 3 --bind unix:/<path_to_django_project_folder>/<socket_filename>.sock <django_project>.wsgi:application

[Install]
WantedBy=multi-user.target

```
* Start gunicorn and enable it to start on boot. After running the commands, make sure that the file <socket_file_name>.sock exists in the project directory. Use the last command to view logs for gunicorn
```
$ sudo systemctl start gunicorn
$ sudo systemctl enable gunicorn
$ sudo journalctl -u gunicorn
```
* Create a webserver configuration file in the /etc/nginx/sites-available/ folder
```
filename: /etc/nginx/sites-available/<filename> 
---
server {
    listen 80;
    server_name <server_domain_or_IP>

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /<path_to_django_project_folder>;
    }
    location /media/ {
        root /<path_to_django_project_folder>;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/<path_to_gunicorn_socket_file>/<socket_filename>.sock;
    }
}
```
* For the above file, create a soft link from the /etc/nginx/sites-available/<filename> folder to the /etc/nginx/sites-enabled/<filename> folder 
```
$ sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```
* Test the Nginx config and restart the service if there are no errors 
```
$ sudo nginx -t
$ sudo systemctl restart nginx
```

This deployment guide is based on [this article from digital ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

### To update the production environment with new changes:
* Update the master branch with the new code
* Stop Nginx and gunicorn running in production
```
$ sudo systemctl stop gunicorn.service
$ sudo systemctl stop nginx.service
```
* Fetch and update the master branch in production
```
$ git fetch
$ git pull 
```
* Migrate any database changes if necessary (Make sure to activate the venv). Run the dev server if needed
```
$ source bin/activate
$ python manage.py makemigrations
$ python manange.py migrate
$ sudo bin/python manage.py runserver 0.0.0.0:80
```
* After verifying the changes in the dev server, reload the daemons, and restart the two services
```
$ sudo systemctl daemon-reload
$ sudo systemctl start gunicorn.service
$ sudo systemctl start nginx.service
```
