from functools import partial

from webargs import ValidationError


def _options_validator(val, options):
    if val not in options:
        raise ValidationError(f'The value `{val}` is not a valid option.')


def options_validator(options=None):
    options = options or []
    return partial(_options_validator, options=options)
