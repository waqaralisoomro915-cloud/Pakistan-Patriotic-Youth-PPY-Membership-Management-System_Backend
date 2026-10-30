
import os
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# -----------------------------
# Phone Number Validation
# -----------------------------

def validate_phone_number(value):
    """
    Accept Pakistani phone numbers:
    03001234567
    +923001234567
    923001234567
    """
    pattern = r"^(?:\+92|92|0)3\d{9}$"

    if not re.fullmatch(pattern, value):
        raise ValidationError(
            _("Enter a valid Pakistani mobile number.")
        )

# -----------------------------
# File Extension Validation
# -----------------------------

def validate_file_extension(value):
    """
    Allow PDF and common image formats.
    """

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    ]

    extension = os.path.splitext(value.name)[1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            _("Only PDF, JPG, JPEG and PNG files are allowed.")
        )


# -----------------------------
# File Size Validation
# -----------------------------

def validate_file_size(value):
    """
    Maximum allowed file size: 5 MB.
    """

    max_size = 5 * 1024 * 1024

    if value.size > max_size:
        raise ValidationError(
            _("File size cannot exceed 5 MB.")
        )


# -----------------------------
# Empty File Validation
# -----------------------------

def validate_non_empty_file(value):
    """
    Prevent empty file uploads.
    """

    if value.size == 0:
        raise ValidationError(
            _("Uploaded file cannot be empty.")
        )
