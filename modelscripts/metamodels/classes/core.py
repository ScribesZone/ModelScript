from modelscripts.metamodels.classes import (
    DataType,
    DataValue
)
from datetime import datetime


def registerDataTypes(model):
    DataType(model, name='String', implementationClass=StringValue)
    DataType(model, name='Integer', implementationClass=IntegerValue)
    DataType(model, name='Real', implementationClass=RealValue)
    DataType(model, name='Boolean', implementationClass=BooleanValue)
    DataType(model, name='Date', implementationClass=DateValue)
    DataType(model, name='DateTime', implementationClass=DateTimeValue)
    DataType(model, name='Time', implementationClass=TimeValue)

def dataTypeFromDataValueName(model, datavalue_name):
    assert datavalue_name.endswith('Value')
    datatype_name=datavalue_name[:-len('Value')]
    return model.dataTypeNamed[datatype_name]


class StringValue(DataValue):

    # TODO: implement isConformToType see YYY

    def __init__(self, stringRepr, type):
        # remove quotes
        value=stringRepr[1:-1]
        super(StringValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class IntegerValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value=int(stringRepr)
        except ValueError:
            raise ValueError(
                'Invalid integer value: "%s"' % stringRepr)
        super(IntegerValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class RealValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value=float(stringRepr)
        except ValueError:
            raise ValueError(
                'Invalid real value: "%s"' % stringRepr)
        super(RealValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class BooleanValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value={
                'true': True,
                'vrai': True,
                'false': False,
                'faux': False
            }[stringRepr]
            self.stringRepr = stringRepr
        except KeyError:
            raise ValueError(
                'Invalid boolean value: "%s"' % stringRepr)
        super(BooleanValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class DateValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(stringRepr, '%d/%m/%Y')
        except ValueError:
            raise ValueError('Invalid date value: "%s"' % stringRepr)
        super(DateValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class DateTimeValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(
                stringRepr,
                '%d/%m/%Y-%H:%M:%S')
        except ValueError:
            raise ValueError('Invalid datetime value: "%s"'
                             % stringRepr)
        super(DateTimeValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class TimeValue(DataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(stringRepr, '%H:%M:%S')
        except ValueError:
            raise ValueError('Invalid time value: "%s"'
                             % stringRepr)
        super(TimeValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )
