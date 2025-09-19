from typing import Annotated, Literal
from pydantic import BaseModel, EmailStr, Field, PlainValidator, validate_call, ConfigDict
import re


def capitalize_name(v: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise ValueError("Имя и фамилия не могут быть пустыми")
    return v.strip().capitalize()

def validate_password(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Пароль должен быть минимум 8 символов")
    if not re.search(r'\d', v):
        raise ValueError("Пароль должен содержать хотя бы 1 цифру")
    if not re.search(r'[!@#$%^&*]', v):
        raise ValueError("Пароль должен содержать хотя бы 1 спецсимвол (!@#$%^&*)")
    return v

NameType = Annotated[
    str,
    PlainValidator(capitalize_name)
]

PasswordType = Annotated[
    str,
    Field(min_length=8, description="Пароль: минимум 8 символов, хотя бы 1 цифра и 1 спецсимвол (!@#$%^&*)"),
    PlainValidator(validate_password)
]

AgeType = Annotated[
    int,
    Field(ge=18, description="Возраст пользователя, минимум 18")
]

RoleType = Literal["admin", "superadmin"]


# ----------------- Модели -----------------
class BaseUser(BaseModel):
    email: EmailStr
    first_name: NameType
    last_name: NameType

    model_config = ConfigDict(
        extra="forbid", # лишние поля при создании объекта
        validate_assignment=True # валидация при изменении значения полей
    )


class User(BaseUser):
    password: PasswordType
    age: AgeType


class AdminUser(User):
    role: RoleType

    @validate_call
    def has_permission(self, permission: str) -> bool:
        if self.role == "superadmin":
            return True
        allowed_permissions = ["read", "write", "delete"]
        return permission in allowed_permissions
