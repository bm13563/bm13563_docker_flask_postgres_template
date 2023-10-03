from celery import Celery

from common.logging import get_logger
from common.config import Config
from common.db_manager import get_global_dbm
from tasks.utils import evaluate_function_from_string


logger = get_logger()
config = Config()
app = Celery("tasks", broker=config.get("BROKER_URL"), include=["tasks"])


def get_celery_worker_status():
    i = app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    return {
        "availability": availability,
        "stats": stats,
        "registered_tasks": registered_tasks,
        "active_tasks": active_tasks,
        "scheduled_tasks": scheduled_tasks,
    }


@app.task
def dispatch_task(cronjob_id, fn):
    dbm = get_global_dbm(config)
    logger.info("applying random wait", extra={"cronjob_id": cronjob_id})
    dbm.execute(
        """
        update cronjobs
        set is_running = true, is_queued = false, last_started = now()
        where cronjob_id = %(cronjob_id)s
    """,
        {"cronjob_id": cronjob_id},
    )
    logger.info("running function", extra={"cronjob_id": cronjob_id})

    try:
        evaluate_function_from_string(fn)()
    except Exception as e:
        logger.error(
            "error running cronjob", extra={"exception": e, "cronjob_id": cronjob_id}
        )

    logger.info("function complete", extra={"cronjob_id": cronjob_id})
    dbm.execute(
        """
        update cronjobs
        set is_running = false, run_now = false, last_completed = now()
        where cronjob_id = %(cronjob_id)s
    """,
        {"cronjob_id": cronjob_id},
    )
