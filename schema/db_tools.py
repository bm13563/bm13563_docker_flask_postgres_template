from subprocess import run
from os import getcwd, listdir, path, mknod, getcwd, remove
from datetime import datetime
import tarfile

from psycopg2.extras import register_uuid

from common.config import Config
from common.db_manager import get_global_dbm
from common.logging import get_logger
from schema.protected_tables import PROTECTED_TABLES


logger = get_logger(__name__)
register_uuid()
config = Config()
dbm = get_global_dbm(config)


MUTEX_ID = "1625475538359"


def migrate():
    migrate_dev()


def migrate_dev():
    logger.info("migrating dev")
    try:
        sorted_sql_files = get_sorted_sql_files()
        _apply_migration(sorted_sql_files)
    except Exception as e:
        logger.error("could not migrate dev environment", extra={"exception": e})
        _release_mutex_lock()
        raise (e)


def _apply_migration(sorted_sql_files: dict):
    logger.info("applying migration")
    _get_mutex_lock()

    result = dbm.fetch_one(
        """
        select exists (
            select from information_schema.tables
            where table_schema = 'migrations'
        )
    """
    )
    migrations_exist = result.get("exists") or False

    if migrations_exist:
        migrations = dbm.fetch_one(
            """
                select max(version)
                from migrations.migrations
            """
        )
        current_version = migrations["max"]
    else:
        current_version = 0

    for version, filename in sorted_sql_files.items():
        if version > current_version:
            with open(
                str(getcwd()) + "/schema/migrations/" + filename, "r"
            ) as sql_file:
                sql = sql_file.read()
                dbm.execute(sql)

    max_version = max(sorted_sql_files.keys())
    dbm.execute(
        """
            insert into migrations.migrations (version) values (%(version)s);
        """,
        {"version": max_version},
    )
    logger.info("migrated to new database version", extra={"version": max_version})

    _release_mutex_lock()


def _get_mutex_lock():
    logger.info("getting mutex lock")
    lock = dbm.fetch_one(
        "select pg_advisory_lock(%(mutex_id)s);", {"mutex_id": MUTEX_ID}
    )
    if not lock:
        raise Exception("could not get lock")
    logger.info("got mutex lock", extra={"mutex_id": MUTEX_ID})


def _release_mutex_lock():
    logger.info("releasing mutex lock")
    dbm.execute("select pg_advisory_unlock(%(mutex_id)s);", {"mutex_id": MUTEX_ID})
    logger.info("released mutex lock", extra={"mutex_id": MUTEX_ID})


def create_db():
    logger.info("creating db")
    migrate_dev()
    restore_db()


def destroy_db():
    logger.info("destroying db")
    dbm.execute("drop schema if exists public cascade;")
    dbm.execute("create schema public;")
    dbm.execute("drop schema if exists migrations cascade;")
    dbm.execute("create schema migrations;")
    logger.info("destroy db")


def get_sorted_sql_files() -> dict:
    logger.info("getting sorted sql files")
    sql_files = listdir(str(getcwd()) + "/schema/migrations")
    sql_files_to_sort = {}
    for f in sql_files:
        if f.endswith(".sql"):
            version = int(f.split("_")[0])
            sql_files_to_sort[version] = f
    return dict(sorted(sql_files_to_sort.items()))


def create_migration(name):
    logger.info("creating migration")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{now}_{name}.sql"
    filepath = f"schema/migrations/{filename}"
    if not path.exists(filepath):
        mknod(filepath)

    with open(filepath, "w") as f:
        f.write("begin;\n\n--add sql below here\n\n\ncommit;\n")


def dump_db():
    # delete from all tables except specified
    all_tables = dbm.fetch(
        """
        select *
        from information_schema.tables
        where table_schema = 'public'
    """
    )

    for table in all_tables:
        table_name = table["table_name"]
        if table_name not in PROTECTED_TABLES:
            logger.debug("deleting table", extra={"table": table})
            dbm.execute(
                f"""
                delete
                from {table_name}
            """
            )

    logger.info("dumping db")
    filename = f"schema/dumps/{datetime.now().strftime('%Y%m%d%H%M%S')}"
    run(
        f"""
        docker exec -t docker_postgres pg_dump --data-only -U postgres > {filename}.dump
    """,
        shell=True,
    )

    with tarfile.open(f"{filename}.tar.gz", "w:gz") as tar:
        tar.add(f"{filename}.dump", arcname=path.basename(f"{filename}.dump"))

    remove(f"{filename}.dump")


def restore_db():
    logger.info("restoring db")
    dump_files = listdir(str(getcwd()) + "/schema/dumps")

    dump_files_to_sort = {}
    for f in dump_files:
        if f.endswith(".tar.gz"):
            version = int(f.split(".")[0])
            dump_files_to_sort[version] = f

    dump_files_sorted = dict(sorted(dump_files_to_sort.items()))
    if len(dump_files_sorted) == 0:
        logger.warning("no files to restore")
        return

    latest_dump = dump_files_sorted[max(dump_files_sorted.keys())]

    with tarfile.open(f"schema/dumps/{latest_dump}", "r:gz") as tar:
        tar.extractall(path="schema/dumps")

    uncompressed_latest_dump = latest_dump.replace(".tar.gz", ".dump")

    run(
        f"""
        docker exec -i docker_postgres psql -U postgres < schema/dumps/{uncompressed_latest_dump};
    """,
        shell=True,
    )

    remove(f"schema/dumps/{uncompressed_latest_dump}")
