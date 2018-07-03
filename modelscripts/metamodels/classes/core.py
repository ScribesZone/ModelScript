from modelscripts.metamodels.classes import (
    DataType,
    DataValue
)


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

    def __init__(self, stringRepr):
        self.value=stringRepr[1:-1]

    def __str__(self):
        if '"' in self.value:
            return "'%s'" % self.value
        else:
            return '"%s"' % self.value


class IntegerValue(DataValue):

    def __init__(self, stringRepr):
        try:
            self.value=int(stringRepr)
        except ValueError:
            raise ValueError(
                'Invalid integer value: "%s"' % stringRepr)

    def __str__(self):
        return str(self.value)


class RealValue(DataValue):

    def __init__(self, stringRepr):
        try:
            self.value=float(stringRepr)
        except ValueError:
            raise ValueError(
                'Invalid real value: "%s"' % stringRepr)

    def __str__(self):
        return str(self.value)


class BooleanValue(DataValue):

    def __init__(self, stringRepr):
        try:
            self.value={
                'true': True,
                'vrai': True,
                'false': False,
                'faux': False
            }[stringRepr]
        except KeyError:
            raise ValueError(
                'Invalid boolean value: "%s"' % stringRepr)

    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'


class DateValue(DataValue):

    def __init__(self, stringRepr):
        self.value=stringRepr

    def __str__(self):
        return str(self.value)


class DateTimeValue(DataValue):

    def __init__(self, stringRepr):
        self.value=stringRepr

    def __str__(self):
        return str(self.value)


class TimeValue(DataValue):

    def __init__(self, stringRepr):
        self.value=stringRepr

    def __str__(self):
        return str(self.value)
