import argparse
import logging

import pytest

from orders.timing import timed


@timed
def echo(args):
    return args.x


@timed
def broken(args):
    raise ValueError("boom")


def test_returns_result_and_passes_args():
    assert echo(argparse.Namespace(x=5)) == 5


def test_keeps_function_name():
    assert echo.__name__ == "echo"


def test_logs_time_at_debug_level(caplog):
    caplog.set_level(logging.DEBUG, logger="orders.timing")

    echo(argparse.Namespace(x=1))

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.DEBUG
    assert "echo" in record.getMessage()


def test_exception_passes_through_and_is_logged(caplog):
    caplog.set_level(logging.DEBUG, logger="orders.timing")

    with pytest.raises(ValueError):
        broken(argparse.Namespace())

    assert "broken" in caplog.text
