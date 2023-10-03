from pytest import fixture

from common.logging import get_logger


logger = get_logger(__name__)


@fixture()
def prepare_db():
    from schema.db_tools import destroy_db, migrate_dev

    destroy_db()
    migrate_dev()
