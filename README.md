
# Configuring Nginx and uWSGI on ubuntu 18.04
```
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```
## Setting virtual environment
```
sudo apt install python3-venv

mkdir ~/project
cd ~/project

python3.6 -m venv projectenv
source projectenv/bin/activate
```
## Configuring Flask
```
pip install wheel
pip install uwsgi flask
```
Creating example object of Flask
```
nano ~/project/project.py
```
Inside of project.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```
## Creating entry point of uWSGI
```
nano ~/project/wsgi.py
```
Inside of wsgi.py
```
from project import app

if __name__ == "__main__":
    app.run()
```
## Configuring uWSGI
```
nano ~/project/project.ini
```  
Inside of project.ini
``` 
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = project.sock
chmod-socket = 660
vacuum = true

die-on-term = true
 ``` 
 ## Configuring files of systemd
```    
sudo nano /etc/systemd/system/project.service
``` 
Inside of project.service
 ``` 
 [Unit]
Description=uWSGI instance to serve project
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/home/username/project
Environment="PATH=/home/username/project/projectenv/bin"
ExecStart=/home/username/project/projectenv/bin/uwsgi --ini /home/username/project/project.ini

[Install]
WantedBy=multi-user.target
 ``` 
Launching
 ``` 
sudo systemctl start project
sudo systemctl enable project
 ``` 
## Configuring Nginx to work with proxy requests
 ``` 
 sudo nano /etc/nginx/sites-available/project
 ``` 
 Inside of project
 ```
 server {
    listen 3000;  #can be any port
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/username/project/project.sock;
    }
}
 ``` 
 
Binding file to sites-enabled directory
 ```
 sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled
 ``` 
 ```
 sudo systemctl restart nginx
 ``` 
## Now you can use your server
 ``` 
Type 0.0.0.0:3000 in your browser
 ``` 
    

