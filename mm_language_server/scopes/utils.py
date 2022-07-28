import re
import warnings
from dataclasses import dataclass
from importlib import import_module
from typing import Callable, Optional

MM_SCOPES = ['mmcls']


@dataclass
class PatternItem:
    pattern: re.Pattern
    registry: Callable
    imports: Optional[Callable] = None


def parse_pattern_list(scope):
    if scope in MM_SCOPES:
        return from_import(f'mm_language_server.scopes.{scope}', 'pattern_list')
    else:
        # TODO
        return None


def from_import(from_, import_, allow_failed_imports=True):
    if not isinstance(from_, str):
        raise TypeError(f'{from_} is of type {type(from_)} and cannot be imported.')
    try:
        mod = import_module(from_)
        imported = getattr(mod, import_)
    except (ImportError, AttributeError):
        if allow_failed_imports:
            warnings.warn(f'Failed to from {from_} import {import_} and is ignored.', UserWarning)
            imported = None
        else:
            raise ImportError(f'Failed to from {from_} import {import_}.')
    return imported


def import_modules(imports, allow_failed_imports=True):
    single_import = False
    if isinstance(imports, str):
        single_import = True
        imports = [imports]
    if not isinstance(imports, list):
        raise TypeError(f'custom_imports must be a list but got type {type(imports)}')

    imported = []
    for imp in imports:
        if not isinstance(imp, str):
            raise TypeError(f'{imp} is of type {type(imp)} and cannot be imported.')
        try:
            imported_tmp = import_module(imp)
        except ImportError:
            if allow_failed_imports:
                warnings.warn(f'{imp} failed to import and is ignored.', UserWarning)
                imported_tmp = None
            else:
                raise ImportError(f'Failed to import {imp}')
        imported.append(imported_tmp)
    if single_import:
        imported = imported[0]
    return imported


def lazy_call(func):

    def wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)

    return wrapper
