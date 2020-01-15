from functools import partial

from webargs import ValidationError


def _enum_validator(val, enum_):
    if val not in enum_.__members__.keys():
        raise ValidationError(f'The value `{val}` is not a valid option.')


def enum_validator(enum_):
    """Takes any number of kwargs where the key is the field name
    and the value is the associated enum
    """
    return partial(_enum_validator, enum_=enum_)
