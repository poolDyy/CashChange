from rest_framework.serializers import ValidationError


__all__ = [
    'validate_password',
]


def validate_password(value: str) -> str:
    """Кастомный валидатор для пароля."""
    if len(value) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов.')

    has_digit = False
    has_upper = False
    has_lower = False

    for char in value:
        if char.isdigit():
            has_digit = True
        elif char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True

        if has_digit and has_upper and has_lower:
            return value

    if not has_digit:
        raise ValidationError('Пароль должен содержать хотя бы одну цифру.')
    if not has_upper:
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
    if not has_lower:
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву.')
