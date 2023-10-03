import pytest

from common.db_manager import get_global_dbm


def test_db_is_up():
    dbm = get_global_dbm()
    assert dbm.is_connected() is True
