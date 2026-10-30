
import uuid
import secrets
import string


def generate_uuid():
    """Generate a unique UUID."""

    return uuid.uuid4()


def generate_unique_code(length=8):
    """
    Generate a random uppercase alphanumeric code.
    Example: A7K92MPL
    """

    characters = string.ascii_uppercase + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def generate_membership_number(prefix="PPY"):
    """
    Generate a membership number.

    Example: PPY-A7K92MPL
    """

    code = generate_unique_code(8)

    return f"{prefix}-{code}"


def get_client_ip(request):
    """
    Get the client's IP address.

    Proxy headers should only be trusted when configured
    behind a trusted proxy.
    """

    return request.META.get("REMOTE_ADDR")
