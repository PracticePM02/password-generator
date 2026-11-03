"""Модуль генерации паролей и оценки их надёжности."""
import math
import secrets
import string

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"

MIN_LENGTH = 4
MAX_LENGTH = 64


class PasswordParamsError(ValueError):
    """Ошибка некорректных параметров генерации."""


def build_alphabet(use_lower=True, use_upper=True, use_digits=True, use_symbols=False):
    """Возвращает список наборов символов, выбранных пользователем."""
    sets = []
    if use_lower:
        sets.append(LOWER)
    if use_upper:
        sets.append(UPPER)
    if use_digits:
        sets.append(DIGITS)
    if use_symbols:
        sets.append(SYMBOLS)
    return sets


def validate_params(length, sets):
    """Проверяет корректность параметров, при ошибке бросает исключение."""
    if not isinstance(length, int):
        raise PasswordParamsError("Длина пароля должна быть целым числом")
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise PasswordParamsError(
            f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH}"
        )
    if not sets:
        raise PasswordParamsError("Выберите хотя бы один набор символов")
    if length < len(sets):
        raise PasswordParamsError("Длина меньше количества выбранных наборов")


def generate_password(length=12, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=False):
    """Генерирует пароль, в котором есть символ из каждого выбранного набора."""
    sets = build_alphabet(use_lower, use_upper, use_digits, use_symbols)
    validate_params(length, sets)

    # По одному символу из каждого набора гарантируем наличие всех типов
    chars = [secrets.choice(s) for s in sets]
    pool = "".join(sets)
    chars += [secrets.choice(pool) for _ in range(length - len(chars))]

    # Перемешиваем, чтобы обязательные символы не стояли в начале
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def estimate_strength(password):
    """Оценивает надёжность. Возвращает (энтропия в битах, текстовая оценка)."""
    if not password:
        return 0.0, "Пусто"

    pool = 0
    if any(c in LOWER for c in password):
        pool += len(LOWER)
    if any(c in UPPER for c in password):
        pool += len(UPPER)
    if any(c in DIGITS for c in password):
        pool += len(DIGITS)
    if any(c in SYMBOLS for c in password):
        pool += len(SYMBOLS)

    entropy = len(password) * math.log2(pool) if pool else 0.0

    if entropy < 40:
        label = "Слабый"
    elif entropy < 60:
        label = "Средний"
    elif entropy < 80:
        label = "Хороший"
    else:
        label = "Отличный"
    return round(entropy, 1), label
