import re

from .utils import PatternItem, from_import, import_modules
from .utils import lazy_call as L

REGISTRY_ROOT = 'mmengine.registry'

pattern_list = [
    # sampler
    PatternItem(
        pattern=re.compile(r'(train|val|test)_dataloader\.sampler\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'DATA_SAMPLERS'),
        imports=L(import_modules)('mmengine.data'),
    ),
    # metrics
    PatternItem(
        pattern=re.compile(r'(train|val|test)_evaluator\.(metrics\.)?type'),
        registry=L(from_import)(REGISTRY_ROOT, 'METRICS'),
        imports=L(import_modules)('mmengine.evaluator'),
    ),
    # optim wrapper
    PatternItem(
        pattern=re.compile(r'optim_wrapper\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'OPTIM_WRAPPERS'),
        imports=L(import_modules)('mmengine.optim'),
    ),
    # optimizer
    PatternItem(
        pattern=re.compile(r'optim_wrapper\.optimizer\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'OPTIMIZERS'),
        imports=L(import_modules)('mmengine.optim'),
    ),
    # paramter scheduler
    PatternItem(
        pattern=re.compile(r'param_scheduler\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'PARAM_SCHEDULERS'),
        imports=L(import_modules)('mmengine.optim'),
    ),
    # hooks
    PatternItem(
        pattern=re.compile(r'default_hooks\.\w+\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'HOOKS'),
        imports=L(import_modules)('mmengine.hooks'),
    ),
]
