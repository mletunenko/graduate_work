import enum


class UserRoleEnum(enum.StrEnum):
    BASIC = "BASIC"
    SUBSCRIBER = "SUBSCRIBER"
    ADMIN = "ADMIN"


class ClientErrorMessage(enum.StrEnum):
    NOT_UNIQUE_EMAIL_ERROR = "Электронная почта уже используется"
    NOT_UNIQUE_PHONE_ERROR = "Телефонный номер уже используется"