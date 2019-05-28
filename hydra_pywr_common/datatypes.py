from . import PywrDataType


parameter_data_type_registry = {}
recorder_data_type_registry = {}


class PywrScenarios(PywrDataType):
    tag = 'PYWR_SCENARIOS'
    name = 'Pywr Scenarios'


class PywrPythonModule(PywrDataType):
    tag = 'PYWR_PY_MODULE'
    name = 'Pywr Python Module'


class PywrNodeOutput(PywrDataType):
    tag = 'PYWR_NODE_OUTPUT'
    name = 'Pywr Node Output'


class PywrParameter(PywrDataType):
    tag = 'PYWR_PARAMETER'
    component = 'parameter'
    name = 'Pywr Parameter'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the component to
        if cls.component is not None:
            parameter_data_type_registry[cls.component] = cls
            parameter_data_type_registry[cls.component.replace('parameter', '')] = cls


class PywrParameterPattern(PywrDataType):
    tag = 'PYWR_PARAMETER_PATTERN'
    name = 'Pywr Parameter Pattern'
    component = None


class PywrParameterPatternReference(PywrParameter):
    tag = 'PYWR_PARAMETER_PATTERN_REF'
    name = 'Pywr Parameter Pattern Reference'
    component = None


class PywrDataframeParameter(PywrParameter):
    tag = 'PYWR_DATAFRAME'
    name = 'Pywr Dataframe'
    component = 'dataframeparameter'


class PywrMonthlyProfileParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_MONTHLY_PROFILE'
    name = 'Pywr Parameter Monthly Profile'
    component = 'monthlyprofileparameter'


class PywrControlCurveIndexParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_CONTROL_CURVE_INDEX'
    name = 'Pywr Parameter Control Curve Index'
    component = 'controlcurveindexparameter'


class PywrIndexedArrayParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_INDEXED_ARRAY'
    name = 'Pywr Parameter Intexed Array'
    component = 'indexedarrayparameter'


class PywrControlCurveInterpolatedParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_CONTROL_CURVE_INTERPOLATED'
    name = 'Pywr Parameter Control Curve Interpolated'
    component = 'controlcurveinterpolatedparameter'


class PywrAggregatedParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_AGGREGATED'
    name = 'Pywr Parameter Aggregated'
    component = 'aggregatedparameter'


class PywrConstantScenarioParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_CONSTANT_SCENARIO'
    name = 'Pywr Parameter Constant Scenario'
    component = 'constantscenarioparameter'




class PywrRecorder(PywrDataType):
    tag = 'PYWR_RECORDER'
    name = 'Pywr Recorder'
    component = 'recorder'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.component is not None:
            recorder_data_type_registry[cls.component] = cls
            recorder_data_type_registry[cls.component.replace('recorder', '')] = cls


class PywrFlowDurationCurveRecorder(PywrRecorder):
    tag = 'PYWR_RECORDER_FDC'
    name = 'Pywr Recorder FDC'
    component = 'flowdurationcurverecorder'


class PywrStorageDurationCurveRecorder(PywrRecorder):
    tag = 'PYWR_RECORDER_SDC'
    name = 'Pywr Recorder SDC'
    component = 'storagedurationcurverecorder'


class PywrFlowDurationCurveDeviationRecorder(PywrRecorder):
    tag = 'PYWR_RECORDER_FDC_DEVIATION'
    name = 'Pywr Recorder FDC Deviation'
    component = 'flowdurationcurvedeviationrecorder'
