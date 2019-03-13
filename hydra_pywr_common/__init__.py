from hydra_base.lib.HydraTypes.Types import Descriptor, Scalar, Array, DataType
import logging
logger = logging.getLogger(__name__)


class PywrDataType(Descriptor):
    tag = 'PYWR_DATA_TYPE'


# Import all types so they are registered with hydra-base
from .datatypes import PywrParameter, PywrMonthlyProfileParameter, parameter_data_type_registry, \
    PywrRecorder, recorder_data_type_registry, PywrPythonModule, PywrParameterPattern, PywrParameterPatternReference


def data_type_from_component_type(component_category, component_type):

    if component_category in ('parameters', 'parameter'):
        registry = parameter_data_type_registry
        fallback_type = PywrParameter
    elif component_category in ('recorders', 'recorder'):
        registry = recorder_data_type_registry
        fallback_type = PywrRecorder
    else:
        raise ValueError('Component category "{}" not recognised.'.format(component_category))

    try:
        data_type = registry[component_type]
    except KeyError:
        data_type = fallback_type
    return data_type


def data_type_from_parameter_value(value):

    if isinstance(value, (int, float)):
        data_type = Scalar
    elif isinstance(value, str):
        data_type = Descriptor
    elif isinstance(value, dict):
        data_type = data_type_from_component_type('parameter', value['type'])
    else:
        raise ValueError(f'Could not determine data type from parameter value: {value}')

    return data_type
