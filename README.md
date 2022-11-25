# Flask-Postgres-Docker template

A "maximal" Flask-Postgres template, containing:

- A Flask app (including auth and JWT support) that can be run in a docker container and under the VSCode debugger
- An NGINX reverse proxy with SSL support
- A Postgres container, that can be accessed using pscyopg2 bindings. No nasty SQLAlchemy
- Migration facilities

The app can be run in two ways - using docker and under the VSCode debugger. The app should behave identically in both environments. It is worth noting that we bypass the NGINX reverse proxy when running in docker or locally - LetsEncrypt requires the endpoint to be publically accessible for SSL to be configured

## Docker usage

You must have Docker and Docker Compose installed on your machine. Run

```bash
bash ctl.sh init
bash ctl.sh build
bash ctl.sh start
```

This will build, and then start, a Flask container and a Postgres container (an empty db) on the same network. The Flask container will be exposed on `localhost:5000`. To add data, run `bash ctl.sh reset`.

This will add data to the Postgres db by running all functions in `schema/data/setup_data.py`. If all of these steps have been run correctly, you should be able to "log in" by POSTing to the `/auth/login` endpoint using the credentials `test_username` and `test_password`:

```bash
curl --location --request POST 'http://127.0.0.1:5000/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test_username",
    "password": "test_password"
}'
```

This will return a non-expiring JWT that can be used to access protected endpoints.

You can stop the Flask and Postgres services by running `bash ctl.sh stop`. 

## Local (VSCode debugger) usage

You must have Python3 installed on your machine (and ideally aliased to `python`). You can then install the python dependencies into a virtual environment:

```bash
python -m venv venv
pip install -e .
pip install -r requirements.txt
source venv/bin/activate
```

Start the docker postgres container by running `bash ctl.sh postgres`. This will run the Postgres container only, and expose it on `localhost:5432`. You can run `bash ctl.sh reset-local` to add data - `bash ctl.sh reset` will not work if the Flask container is not running, so it is important not conflate these commands.

You should then go to the debug panel in VSCode, select the "Run server" script and press "Start debugging" (or F5)

## Migrations

Migrations are supported out-of-the-box. Migrations are run automatically when running `bash ctl.sh reset` or `bash ctl.sh reset-local`. If you want to run a standalone migration (e.g in prod) you can run `bash db.sh migrate`. To add a new migration, run `bash db.sh create-migration <NAME OF MIGRATION>`. This will create a new migration in the `schema/migrations` directory
