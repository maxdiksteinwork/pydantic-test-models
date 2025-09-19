import pydantic_core
import pytest
from models import BaseUser, User, AdminUser

# ----------------- baseuser -----------------
# позитивные тесты
@pytest.mark.parametrize("first_name,last_name", [
    ("Петя", "Иванов"),
    ("петя", "иванов"),
])
def test_baseuser_names_valid(first_name, last_name):
    u = BaseUser(email="a@b.com", first_name=first_name, last_name=last_name)
    assert u.first_name[0].isupper()
    assert u.last_name[0].isupper()

# негативные тесты
@pytest.mark.parametrize("first_name,last_name", [
    ("", "Иванов"),
    ("   ", "Иванов"),
])
def test_baseuser_names_invalid(first_name, last_name):
    with pytest.raises(ValueError):
        BaseUser(email="a@b.com", first_name=first_name, last_name=last_name)

def test_baseuser_invalid_email():
    with pytest.raises(ValueError):
        BaseUser(email="invalid-email", first_name="Петя", last_name="Иванов")

def test_baseuser_extra_field_forbid():
    with pytest.raises(ValueError):
        BaseUser(email="a@b.com", first_name="Петя", last_name="Иванов", extra="x")

# ----------------- user -----------------
# позитивные тесты пароля
@pytest.mark.parametrize("password", [
    "Abcdef1!",
    "Password123!"
])
def test_user_password_valid(password):
    u = User(email="a@b.com", first_name="Иван", last_name="Петров",
             password=password, age=25)
    assert u.password == password

# негативные тесты пароля
@pytest.mark.parametrize("password", [
    "Abcdefgh!",   # нет цифры
    "Abcd1234",    # нет спецсимвола
    "A1!",         # <8 символов
])
def test_user_password_invalid(password):
    with pytest.raises(ValueError):
        User(email="a@b.com", first_name="Иван", last_name="Петров",
             password=password, age=25)

# позитивные тесты возраста
@pytest.mark.parametrize("age", [18, 19, 25])
def test_user_age_valid(age):
    u = User(email="a@b.com", first_name="Иван", last_name="Петров",
             password="Abcd1234!", age=age)
    assert u.age == age

# негативные тесты возраста
@pytest.mark.parametrize("age", [17, 0, -5])
def test_user_age_invalid(age):
    with pytest.raises(ValueError):
        User(email="a@b.com", first_name="Иван", last_name="Петров",
             password="Abcd1234!", age=age)

# негативный тест валидации при изменении полей
def test_assignment_validation_age():
    u = User(email="a@b.com", first_name="Иван", last_name="Петров",
             password="Abcd1234!", age=25)
    with pytest.raises(ValueError):
        u.age = 17

# ----------------- adminuser -----------------
# позитивные тесты метода has_permission
@pytest.mark.parametrize("role,permission", [
    ("admin", "read"),
    ("admin", "delete"),
    ("superadmin", "read"),
    ("superadmin", "ban"),
])
def test_admin_has_permission_valid(role, permission):
    admin = AdminUser(email="a@b.com", first_name="Вася", last_name="Петров",
                      password="Abcd1234!", age=35, role=role)
    assert admin.has_permission(permission) is True

# негативные тесты роли и метода
def test_adminuser_invalid_role():
    with pytest.raises(ValueError):
        AdminUser(email="a@b.com", first_name="Вася", last_name="Петров",
                  password="Abcd1234!", age=35, role="moderator")

def test_admin_has_permission_wrong_type():
    admin = AdminUser(email="a@b.com", first_name="Вася", last_name="Петров",
                      password="Abcd1234!", age=35, role="admin")
    with pytest.raises(pydantic_core.ValidationError):
        admin.has_permission(123)  # int вместо str