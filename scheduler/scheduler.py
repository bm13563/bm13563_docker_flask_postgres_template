from random import randint
from time import sleep
from datetime import datetime

from croniter import croniter

from common.logging import get_logger
from common.config import Config
from common.db_manager import get_global_dbm
from tasks.celery import dispatch_task, get_celery_worker_status


config = Config()
dbm = get_global_dbm(config)
logger = get_logger()


def _run_cronjob(cronjob):
    logger.info("running cronjob", extra={"cronjob_id": cronjob["cronjob_id"]})
    cronjob_id = cronjob["cronjob_id"]
    cronjob_path = cronjob["path"]
    randomness = cronjob["randomness"]

    if randomness > 0:
        wait_time = randint(0, randomness)
    else:
        wait_time = 0

    logger.info(
        "dispatching task", extra={"cronjob_id": cronjob_id, "wait_time": wait_time}
    )
    dispatch_task.apply_async(args=(cronjob_id, cronjob_path), countdown=wait_time)

    dbm.execute(
        """
        update cronjobs
        set is_queued = true, last_queued = now()
        where cronjob_id = %(cronjob_id)s
    """,
        {"cronjob_id": cronjob_id},
    )


def _should_run_cronjob(cronjob):
    logger.info("checking if cronjob should run")
    schedule = cronjob["schedule"]

    if cronjob.get("last_completed") is None:
        return True

    cron = croniter(schedule, cronjob["last_completed"])
    _next = cron.get_next(datetime).replace(tzinfo=None)
    _now = datetime.now()
    logger.info(
        "next run",
        extra={
            "next": _next.strftime("%Y-%m-%d %H:%M:%S"),
            "now": _now.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )
    return _next <= _now


def _get_cronjobs():
    logger.info("getting cronjobs")
    return dbm.fetch(
        """
        select *
        from cronjobs
        where is_active is true
            and is_running is false
            and is_queued is false
    """
    )


def _get_on_demand_cronjobs():
    logger.info("getting on demand cronjobs")
    return dbm.fetch(
        """
        select *
        from cronjobs
        where run_now is true
            and is_active is true
            and is_running is false
            and is_queued is false
    """
    )


if __name__ == "__main__":
    logger.info("scheduler started")
    logger.info(get_celery_worker_status())
    while True:
        if get_celery_worker_status()["availability"] is None:
            logger.warning("no celery workers available, no-op")
            sleep(1)
        else:
            cronjobs = _get_cronjobs()

            for cronjob in cronjobs:
                if _should_run_cronjob(cronjob):
                    logger.info(
                        "cronjob should run",
                        extra={"cronjob_id": cronjob["cronjob_id"]},
                    )
                    _run_cronjob(cronjob)

            on_demand_cronjobs = _get_on_demand_cronjobs()
            for cronjob in on_demand_cronjobs:
                logger.info(
                    "on demand cronjob should run",
                    extra={"cronjob_id": cronjob["cronjob_id"]},
                )
                _run_cronjob(cronjob)

            sleep(1)
