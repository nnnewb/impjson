import json
import logging
import os
import sys
from importlib.abc import PathEntryFinder, Loader
from importlib.machinery import ModuleSpec
from pathlib import PurePath
from types import ModuleType


class JSONImporter(PathEntryFinder, Loader):

    def __init__(self):
        super().__init__()
        self.cached_module_specs = {}

    def module_repr(self, module):
        return module.__doc__

    def load_module(self, fullname, *, _fallback_find_spec=True):
        try:
            path = self.cached_module_specs[fullname].origin
            with open(path, 'r') as f:
                content = f.read()
                m = ModuleType(name=fullname.split('.')[-1], doc=content)
                m.__file__ = path
                m.__name__ = fullname
                m.__loader__ = self
                sys.modules[fullname] = m
                loaded = json.loads(content)
                if isinstance(loaded, (int, float, str, list, type(None))):
                    m.value = loaded
                else:
                    for k, v in loaded.items():
                        setattr(m, k, v)
                return m

        except KeyError:
            if _fallback_find_spec:
                self.find_spec(fullname)
                return self.load_module(fullname, _fallback_find_spec=False)

    def find_spec(self, fullname, target=None, unknown=None):
        dir_list = target if target else sys.path
        name = fullname.split('.')[-1]

        for dir_name in dir_list:
            if target:
                path = PurePath(dir_name).joinpath(f'{name}.json')
            else:
                path = PurePath(dir_name).joinpath(*fullname.split('.')[:-1], f'{name}.json')

            if os.path.exists(path):
                self.cached_module_specs[fullname] = ModuleSpec(fullname, self, origin=path)
                break

        return self.cached_module_specs.get(fullname)


def install(force=False):
    """ install JSON importer

    :param force: force reinstall the JSON importer
    :return: True if install successful, otherwise False
    """
    logger = logging.getLogger(__name__)

    if force:
        all_installed = [imp for imp in filter(lambda imp: isinstance(imp, JSONImporter), sys.meta_path)]
        for installed in all_installed:
            sys.meta_path.remove(installed)
        sys.meta_path.append(JSONImporter())
    else:
        if any(map(lambda imp: isinstance(imp, JSONImporter), sys.meta_path)):
            logger.warning('JSON Importer has already installed, you can do `install(force=True)` reinstall it.')
            return False
        else:
            sys.meta_path.append(JSONImporter())

    return True
