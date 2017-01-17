import sys, builtins, itertools, traceback, functools
import re
import importlib
from importlib import import_module, find_loader
from inspect import currentframe, getouterframes, stack, getmodule


VER_SOURCE_RE = re.compile(r'(.*example/)(v\d+)(/.*\.py)')
VER_MODULE_RE = re.compile(r'(example\.)(v\d+)(\..*)')


class PyOFimporter(object):

    # def __init__(self):
    #     self.pyof_modules = {}

    def _add_module(self, mod, *fullnames):
        for fullname in fullnames:
            sys.modules[fullname] = mod
            # self.pyof_modules[fullname] = mod

    def _get_module(self, fullname):
        print("_get_module(", fullname, ")")
        return sys.modules.get(fullname)
        # return self.pyof_modules.get(fullname)

    def __get_module(self, fullname):
        print("__get_module(", fullname, ")")
        try:
            return sys.modules[fullname]
            # return self.pyof_modules[fullname]
        except KeyError:
            raise ImportError("This loader does not know module " + fullname)

    def find_module(self, module_name, package_path=None):
        print('finding: ', module_name, package_path)
        if not module_name.startswith('example.v'):
            return None

        caller = self._get_caller_data()
        requested = self._get_requested_data(module_name)

        if (caller is not None and requested is not None and
            caller.get('module') != requested.get('module') and
            caller.get('version') != requested.get('version')):
            return self
        else:
            # Let the default python import handle this
            return None

    def load_module(self, module_name):
        print("Loading module: ", module_name)
        caller = self._get_caller_data()
        requested = self._get_requested_data(module_name)

        if (caller is not None and requested is not None and
            caller.get('module') != requested.get('module') and
            caller.get('version') != requested.get('version')):
            # print("Caller_module: {}".format(caller.get('module')))
            # print("Caller_version: {}".format(caller.get('version')))
            # print("Requested Module: ", requested.get('module'))
            # print("Requested Version: ", requested.get('version'))
            new_module_name = module_name.replace(requested.get('version'),
                                                  caller.get('version'))
            # print("Actually Importing {} instead of {}".format(caller.get('version') + requested.get('module'),
            #                                                    requested.get('version') + requested.get('module')))


        # print('--------------')
        # [print(key, ": ", sys.modules[key]) for key in sys.modules if key.startswith('example')]
        # print('--------------')
        print("Importing: ", new_module_name)
        builtins.__import__(new_module_name)
        mod = sys.modules[new_module_name]
        mod.__loader__ = self
        sys.modules[new_module_name] = mod
        sys.modules[module_name] = sys.modules[new_module_name]
        # [print(key, ": ", sys.modules[key]) for key in sys.modules if key.startswith('example')]
        return sys.modules[new_module_name]

    @staticmethod
    def _get_requested_data(module_name):
        version = None
        module = None
        requested = VER_MODULE_RE.match(module_name)
        if requested:
            version = requested.group(2)
            module = requested.group(3)
            return {'module': module, 'version': version}
        return None

    @staticmethod
    def _get_caller_data():
        version = None
        module = None
        outer_frames = getouterframes(currentframe())
        for frame in outer_frames[::-1]:
            filename = frame.filename
            matched = VER_SOURCE_RE.match(filename)
            if matched:
                version = matched.group(2)
                module = matched.group(3).replace('/', '.').rstrip('\.py')
                return {'module': module, 'version': version}
        return None

    def is_package(self, fullname):
        """
        Return true, if the named module is a package.
        We need this method to get correct spec objects with
        Python 3.4 (see PEP451)
        """
        return hasattr(self.__get_module(fullname), "__path__")

    def get_code(self, fullname):
        """Return None
        Required, if is_package is implemented"""
        self.__get_module(fullname)  # eventually raises ImportError
        return None

    get_source = get_code  # same as get_code


sys.meta_path.insert(0, PyOFimporter())
