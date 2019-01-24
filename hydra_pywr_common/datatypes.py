from . import PywrDataType


parameter_data_type_registry = {}
recorder_data_type_registry = {}


class PywrPythonModule(PywrDataType):
    tag = 'PYWR_PY_MODULE'




class PywrParameter(PywrDataType):
    tag = 'PYWR_PARAMETER'
    component = 'parameter'

    editors = [
        {
            "type": "ace",
            "mode": "JSON"
        }
    ]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register the component to
        parameter_data_type_registry[cls.component] = cls


class PywrParameterPattern(PywrParameter):
    tag = 'PYWR_PARAMETER_PATTERN'


class PywrParameterPatternReference(PywrParameter):
    tag = 'PYWR_PARAMETER_PATTERN_REF'


class PywrMonthlyProfileParameter(PywrParameter):
    tag = 'PYWR_PARAMETER_MONTHLY_PROFILE'
    component = 'monthlyprofileparameter'

    editors = [
        {
            "type": "form",
            "schema": {
                "values": {
                    "type": "handsontable",
                    "title": "Values",
                    "rows": 12,
                    "row_labels": 'JFM...'
                },
                "comment": {
                    "type": "string",
                    "title": "Comment",
                    "format": "text"
                },
            }
        },
        {
            "type": "plotly",
            "attribute": "__result__"
        },
        {
            "type": "html/docs/text/md",
            "content": 'The awesome documentation about this data type ...',
        },
        {
            "type": "ace",
            "mode": "JSON"
        }
    ]





class PywrRecorder(PywrDataType):
    tag = 'PYWR_RECORDER'
    component = 'recorder'

    editors = [
        {
            "type": "ace",
            "mode": "JSON"
        }
    ]

    def __init_subclass__(cls, **kwargs):
        # Register the component to
        recorder_data_type_registry[cls.component] = cls
