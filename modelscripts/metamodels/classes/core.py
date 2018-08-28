from modelscripts.metamodels.classes.types import DataType, DataValue
from datetime import datetime


def registerDataTypes(model):
    DataType(model,
             name='String',
             implementationClass=StringValue,
             isCore=True)
    DataType(model,
             name='Integer',
             implementationClass=IntegerValue,
             isCore = True)
    DataType(model,
             name='Real',
             implementationClass=RealValue,
             isCore=True)
    DataType(model,
             name='Boolean',
             implementationClass=BooleanValue,
             isCore=True)
    DataType(model,
             name='Date',
             implementationClass=DateValue,
             isCore=True)
    DataType(model,
             name='DateTime',
             implementationClass=DateTimeValue,
             isCore=True)
    DataType(model,
             name='Time',
             implementationClass=TimeValue,
             isCore=True)
    DataType(model,
             name='NullType',
             implementationClass=NullTypeValue,
             isCore=True)

def dataTypeFromDataValueName(model, datavalue_name):
    assert datavalue_name.endswith('Value')
    datatype_name=datavalue_name[:-len('Value')]
    return model.dataType(datatype_name)


class CoreDataValue(DataValue):

    @property
    def isCore(self):
        return True


class NullTypeValue(CoreDataValue):

    # TODO:3 implement isConformToType see YYY

    def __init__(self, stringRepr, type):
        # remove quotes
        value=stringRepr[1:-1]
        super(NullTypeValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class StringValue(CoreDataValue):

    # TODO:3 implement isConformToType see YYY

    def __init__(self, stringRepr, type):
        # remove quotes
        value=stringRepr[1:-1]
        super(StringValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class IntegerValue(CoreDataValue):

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


class RealValue(CoreDataValue):

    def __init__(self, stringRepr, type):
        try:
            value=float(stringRepr)
        except ValueError:
            raise ValueError( #raise:TODO:2
                'Invalid real value: "%s"' % stringRepr)
        super(RealValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class BooleanValue(CoreDataValue):

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
            raise ValueError(  #raise:TODO:2
                'Invalid boolean value: "%s"' % stringRepr)
        super(BooleanValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class DateValue(CoreDataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(stringRepr, '%d/%m/%Y')
        except ValueError:
            raise ValueError(  #raise:TODO:2
                'Invalid date value: "%s"' % stringRepr)
        super(DateValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class DateTimeValue(CoreDataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(
                stringRepr,
                '%d/%m/%Y-%H:%M:%S')
        except ValueError:
            raise ValueError(  #raise:TODO:2
                'Invalid datetime value: "%s"' % stringRepr)
        super(DateTimeValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


class TimeValue(CoreDataValue):

    def __init__(self, stringRepr, type):
        try:
            value = datetime.strptime(stringRepr, '%H:%M:%S')
        except ValueError:
            raise ValueError(  #raise:TODO:2
                'Invalid time value: "%s"'
                 % stringRepr)
        super(TimeValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )
