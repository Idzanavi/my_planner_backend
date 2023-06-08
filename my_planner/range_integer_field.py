from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RangeIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.pop("validators", [])
        min_value = kwargs.pop("min_value", None)
        max_value = kwargs.pop("max_value", None)
        if min_value is not None:
            validators.append(MinValueValidator(min_value))
        if max_value is not None:
            validators.append(MaxValueValidator(max_value))
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)

