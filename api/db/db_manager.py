from time import sleep

from psycopg2 import connect
from psycopg2.extras import RealDictCursor, register_uuid

from api.config import config
from common.logging import get_logger


logger = get_logger()


test = config.get("DB_HOST")


class DbManager:
    def __init__(self):
        register_uuid()
        self.db = self._connect()

    def _connect(self):
        attempts = 0
        while attempts < 5:
            try:
                logger.info(
                    "attempting to connect to db",
                    extra={
                        "host": config.get("DB_HOST"),
                        "database": config.get("DB_DATABASE"),
                        "user": config.get("DB_USERNAME"),
                    },
                )
                connection = connect(
                    host=config.get("DB_HOST"),
                    database=config.get("DB_DATABASE"),
                    user=config.get("DB_USERNAME"),
                    password=config.get("DB_PASSWORD"),
                )
                self.db = connection
                logger.info(
                    "connected to db",
                    extra={
                        "host": config.get("DB_HOST"),
                        "database": config.get("DB_DATABASE"),
                        "user": config.get("DB_USERNAME"),
                    },
                )
                return connection
            except Exception as e:
                attempts += 1
                logger.warn(
                    "failed to connect to database, retrying",
                    extra={
                        "attempt": attempts,
                        "exception": e,
                    },
                )
                sleep(1)
        else:
            logger.error("failed to connect to database, exiting")
            exit(1)

    def _ensure_connected(self):
        if self.db.closed > 0:
            self.db = connect()

    def _execute(self, cursor, query, params=None):
        self._ensure_connected()
        try:
            logger.info("executing query", extra={"query": query, "params": params})
            cursor.execute(query, params)
            self.db.commit()
        except Exception as e:
            logger.error(
                "failed to execute query",
                extra={"query": query, "params": params, "exception": e},
            )
            self.db.rollback()
            raise (e)
        return cursor

    def execute(self, query, params=None):
        cursor = self.db.cursor()
        self._execute(cursor, query, params)
        return cursor

    def fetch(self, query, params=None):
        cursor = self.db.cursor(cursor_factory=RealDictCursor)
        self._execute(cursor, query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.db.cursor(cursor_factory=RealDictCursor)
        self._execute(cursor, query, params)
        return cursor.fetchone()
