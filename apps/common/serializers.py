
from rest_framework import serializers

from .validators import (validate_phone_number,validate_file_extension,validate_file_size, validate_non_empty_file,)


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Common parent for PPY model serializers.
    """
    class Meta:
        abstract = True


class PhoneNumberField(serializers.CharField):
    """
    Reusable Pakistani phone number field.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 13)
        kwargs.setdefault("trim_whitespace", True)

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        validate_phone_number(value)
        return value


class DocumentFileField(serializers.FileField):
    """
    Reusable document upload field.
    Allows PDF, JPG, JPEG and PNG up to 5 MB.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("allow_empty_file", False)

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)

        validate_non_empty_file(value)
        validate_file_extension(value)
        validate_file_size(value)

        return value
