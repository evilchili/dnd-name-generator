import importlib
import os
import pkgutil
import sys

from types import ModuleType

language_pack = None
supported_languages = None


def _import_submodules(module):
    pkgs = pkgutil.iter_modules(module.__path__)
    for loader, module_name, is_pkg in pkgs:
        yield importlib.import_module(f"{module.__name__}.{module_name}")


def load_language_pack(module_name: str = "") -> ModuleType:
    if not module_name:
        module_name = os.getenv("FANLANG_LANGUAGE_PACK", "language.languages")
    language_pack = importlib.import_module(module_name)
    _import_submodules(language_pack)
    supported_languages = dict(
        (module.__name__.split(".")[-1], module) for module in list(_import_submodules(sys.modules[module_name]))
    )
    return language_pack, supported_languages
