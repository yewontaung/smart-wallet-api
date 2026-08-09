from enum import Enum


class SignInWith(str, Enum):
    PHONE = "Phone"
    EMAIL = "Email"