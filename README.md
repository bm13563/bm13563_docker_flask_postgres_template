# Flask-Postgres-Docker template

This repo is a template containing:

- A Flask API configured to run in a docker container. This contains
  - a database manager
  - linting
  - logging
- A Postgres instance configured to run in a docker container. This contains
  - migration tooling
  - functionality for setting up test data in a local database

## Dependencies

Theoretically only docker and python 3. This was developed on Ubuntu 20.04 - no idea how it will behave on other OS. The containers are currently set up with a default name which will need to be changed

## Setting up

Pull Postgres image and build Flask server:

```bash
. ctl init
. ctl build
```

## Running

Run Flask and Postgres in docker:

```bash
. ctl start
```

Stop Flask and Postgres in Docker:

```bash
. ctl stop
```

Destroy Postgres container:

```bash
. ctl reset
```

## Migrations

Build the db locally and populate with test data (from `schema/data/`):

```bash
. db create-db
```

Reset the db locally:

```bash
. db reset-db
```

Create a new migration:

```bash
. db create-migration <MIGRATION_NAME>
```

Execute a migration:

```bash
. db migrate
```
