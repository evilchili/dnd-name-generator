import importlib
import pkgutil
import sys


def import_submodules(module):
    pkgs = pkgutil.iter_modules(module.__path__)
    for loader, module_name, is_pkg in pkgs:
        yield importlib.import_module(f"{module.__name__}.{module_name}")


supported_languages = dict(
    (module.__name__.split(".")[-1], module) for module in list(import_submodules(sys.modules[__name__]))
)
