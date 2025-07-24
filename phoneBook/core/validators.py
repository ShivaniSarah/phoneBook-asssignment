# core/validators.py

import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


class Validator:
    PHONE_REGEX = re.compile(r'^\+91\d{10}$')

    @classmethod
    def validate_phone(cls, phone: str) -> bool:
        return bool(cls.PHONE_REGEX.match(phone.strip()))

    @staticmethod
    def normalize_phone(phone: str) -> str:
        phone = phone.strip().replace(" ", "")
        if not phone.startswith("+"):
            if phone.startswith("91") and len(phone) == 12:
                return "+" + phone
            elif len(phone) == 10 and phone.isdigit():
                return "+91" + phone
        return phone

    @staticmethod
    def validate_email_format(email: str) -> bool:
        try:
            django_validate_email(email.strip())
            return True
        except ValidationError:
            return False
