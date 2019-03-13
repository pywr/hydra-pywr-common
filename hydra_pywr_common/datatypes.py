from . import PywrDataType


parameter_data_type_registry = {}
recorder_data_type_registry = {}


class PywrPythonModule(PywrDataType):
    tag = 'PYWR_PY_MODULE'


class PywrParameter(PywrDataType):
    tag = 'PYWR_PARAMETER'
    component = 'parameter'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the component to
        if cls.component is not None:
            parameter_data_type_registry[cls.component] = cls
            parameter_data_type_registry[cls.component.replace('parameter', '')] = cls


class PywrParameterPattern(PywrParameter):
    tag = 'PYWR_PARAMETER_PATTERN'
    component = None


class PywrParameterPatternReference(PywrParameter):
    tag = 'PYWR_PARAMETER_PATTERN_REF'
    component = None


class PywrMonthlyProfileParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_MONTHLY_PROFILE'
    component = 'monthlyprofileparameter'


class PywrControlCurveIndexParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_CONTROL_CURVE_INDEX'
    component = 'controlcurveindexparameter'


class PywrIndexedArrayParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_INDEXED_ARRAY'
    component = 'indexedarrayparameter'


class PywrRecorder(PywrDataType):
    tag = 'PYWR_RECORDER'
    component = 'recorder'

    def __init_subclass__(cls, **kwargs):
        # Register the component to
        recorder_data_type_registry[cls.component] = cls
