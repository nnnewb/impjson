import os
import sys

import pytest


@pytest.fixture()
def add_tests_folder_as_search_path():
    sys.path.append(os.path.dirname(__file__))
    yield
    sys.path.pop(-1)


def test_import_relative():
    from . import data
    assert data.name == 'hello world'


def test_import_absolute():
    from tests import data
    assert data.name == 'hello world'


@pytest.mark.usefixtures('add_tests_folder_as_search_path')
def test_import_direct():
    import data
    assert data.name == 'hello world'


def test_import_direct_not_in_search_path():
    with pytest.raises(ImportError):
        import data
