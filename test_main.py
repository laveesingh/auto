#! /usr/bin/python3

from auto import io_utils


def test_logger():
    logger = io_utils.Logger(say=True)
    logger.alert('The quick brown fox jumped over a lazy dog')
    logger.success('We are successful Lavee!')
    assert True
