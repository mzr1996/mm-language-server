import re

from .utils import PatternItem, from_import, import_modules
from .utils import lazy_call as L

REGISTRY_ROOT = 'mmcls.registry'

pattern_list = [
    # model
    PatternItem(
        pattern=re.compile(r'model\.(backbone\.|neck\.|head\.)?type'),
        registry=L(from_import)(REGISTRY_ROOT, 'MODELS'),
        imports=L(import_modules)('mmcls.models'),
    ),
    # init cfg
    PatternItem(
        pattern=re.compile(r'model\.(.*)\.init_cfg'),
        registry=L(from_import)(REGISTRY_ROOT, 'WEIGHT_INITIALIZERS'),
        imports=L(import_modules)('mmcls.engine'),
    ),
    # dataset
    PatternItem(
        pattern=re.compile(r'(train|val|test)_dataloader\.dataset\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'DATASETS'),
        imports=L(import_modules)('mmcls.datasets'),
    ),
    # pipeline
    PatternItem(
        pattern=re.compile(r'(train|val|test)_dataloader\.dataset\.pipeline\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'TRANSFORMS'),
        imports=L(import_modules)('mmcls.datasets'),
    ),
    PatternItem(
        pattern=re.compile(r'(train|val|test)_pipeline\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'TRANSFORMS'),
        imports=L(import_modules)('mmcls.datasets'),
    ),
    # sampler
    PatternItem(
        pattern=re.compile(r'(train|val|test)_dataloader\.sampler\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'DATA_SAMPLERS'),
        imports=L(import_modules)('mmcls.datasets'),
    ),
    # metrics
    PatternItem(
        pattern=re.compile(r'(train|val|test)_evaluator\.(metrics\.)?type'),
        registry=L(from_import)(REGISTRY_ROOT, 'METRICS'),
        imports=L(import_modules)('mmcls.evaluation'),
    ),
    # optim wrapper
    PatternItem(
        pattern=re.compile(r'optim_wrapper\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'OPTIM_WRAPPERS'),
        imports=L(import_modules)('mmcls.engine'),
    ),
    # optimizer
    PatternItem(
        pattern=re.compile(r'optim_wrapper\.optimizer\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'OPTIMIZERS'),
        imports=L(import_modules)('mmcls.engine'),
    ),
    # paramter scheduler
    PatternItem(
        pattern=re.compile(r'param_scheduler\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'PARAM_SCHEDULERS'),
        imports=L(import_modules)('mmcls.engine'),
    ),
    # hooks
    PatternItem(
        pattern=re.compile(r'default_hooks\.\w+\.type'),
        registry=L(from_import)(REGISTRY_ROOT, 'HOOKS'),
        imports=L(import_modules)('mmcls.engine'),
    ),
]
