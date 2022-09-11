# Flask-Postgres-Docker template

This repo is a template containing:

1. A Flask API configured to run in a docker container. This contains
  a. a database manager
  b. linting
  c. logging
2. A Postgres instance configured to run in a docker container. This contains
  a. migration tooling
  b. functionality for setting up test data in a local database

## Dependencies

Theoretically, just docker and python 3. This was developed on Ubuntu 20.04 - no idea how it will behave on other OS

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
