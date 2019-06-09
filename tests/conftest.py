import sys

import pytest


@pytest.fixture(scope='function', autouse=True)
def add_importer():
    from impjson import JSONImporter
    sys.meta_path.append(JSONImporter())
    yield
    sys.meta_path.pop(-1)


@pytest.fixture(scope='function', autouse=True)
def cleanup_cached_module():
    from sys import modules
    modules.pop('data', None)
    modules.pop('tests.data', None)
