# ZB MED Article Evaluation App

## Development

To try the app locally on your computer:
- Open up a terminal window.
- Clone the repository with `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance/tree/web-app`
- Go to the `TREC-doc-2-doc-relevance` folder and open the terminal.
- Type:
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Output:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```
- Visit `http://127.0.0.1:5000/` in your browser of choice (Firefox, Chrome, Edge, Safari) and the app should be up and running.

To enable the virtual environment:
- Go to the `app` folder.
- Type in the terminal `. venv/bin/activate`

To install setup.py:
- Go to the `TREC-doc-2-doc-relevance` folder
- Type in the terminal `pip install -e .` to install setup.py which will solve the problem of relative paths.

## Deployment

These instructions are for deployment without the use of docker, if you're planning to deploy this project using docker,
please follow the steps described at `docker-img/READM.md`.

The guide assumes that the VM used for deployment is correctly configured and accessible from a port such as HTTP or HTTPS.

The information has been primarily retrieved from [this guide](https://pythonise.com/series/learning-flask/deploy-a-flask-app-nginx-uwsgi-virtual-machine).

- Clone the repository
    - Run `git clone https://github.com/zbmed-semtec/TREC-doc-2-doc-relevance.git` to copy the directoy onto your machine.
    - Create `/clone-dir/app.ini`. You could copy the one used in the article [from GitHub](https://github.com/Julian-Nash/simple-flask-demo/blob/master/app.ini)
    - Change your directory to `TREC-doc-2-doc-relevance`
- Set up the development environment
    - Make sure that a version of Python (> 3.0) is available on your machine.
    - `sudo apt-get update`
    - `sudo apt-get install python-venv`
    - `python -m venv venv-name`
    - `source venv-name/bin/activate`
    - `sudo apt install python-pip`
    - `pip install --upgrade pip`
    - `pip install -r requirements.txt`
    - `pip install uwsgi`
- Create Systemd service
    - `sudo nano /etc/systemd/system/app.service`
    - Insert the following block segment, replace `_USER_` with your machine's user account:
    ```
    [Unit]
    Description=TREC doc2doc relevance assesment application.
    After=network.target

    [Service]
    User=_USER_
    Group=www-data
    WorkingDirectory=/home/_USER_/TREC-doc-2-doc-relevance/
    Environment="PATH=/home/_USER_/TREC-doc-2-doc-relevance/venv-name/bin"
    ExecStart=/home/_USER_/TREC-doc-2-doc-relevance/venv-name/bin/uwsgi --ini app.ini

    [Install]
    WantedBy=multi-user.target
    ```
    - `sudo systemctl start app`
    - `sudo systemctl enable app`
- Configure nginx
    - `sudo apt install nginx-full`
    - `sudo nano /etc/nginx/sites-available/app`
    - Insert the following block segment, where `XXXXX` is your assigned port number (e.g. port 80 for HTTP) and `YYYYYY` your machine's external IP address:
    ```
    server {
        listen XXXXX default_server;
        server_name YYYYY;
        client_max_body_size 100M;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:/home/_USER_/TREC-doc-2-doc-relevance/app.sock;
        }
    }
    ```
    - `sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled`
    - `sudo systemctl restart nginx`