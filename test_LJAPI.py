# coding=utf-8
"""Test get json."""
import os


from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from conftest import dbtransaction


def test_get_json():
    """Test to make sure we are getting correct data from API."""
    from .LJAPI import get_json
    test = get_json()
    for entry in test:
        if "David Flegal" in entry['title']:
            return entry
        else:
            pass
    assert "David Flegal" in entry['title']


def test_search_and_create(dbtransaction):
    """Test the search function."""
    from .LJAPI import search_and_create
    assert search_and_create("bob", "chicken") is False
