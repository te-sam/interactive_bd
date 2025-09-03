"""Модуль для работы с БД.

Предоставляет функции для работы с БД.
"""

from utils import get_current_state

values = {}
transaction_stack = []


def set_value(key: str, value: str) -> None:
    """Добавление новой записи в БД.

    Args:
        key: ключ
        value: значение
    """
    if transaction_stack:
        current_transaction = transaction_stack[-1]
        if key in current_transaction["deleted"]:
            current_transaction["deleted"].remove(key)
        current_transaction["changes"][key] = value
    else:
        values[key] = value


def unset_value(key: str) -> None:
    """Удаление записи из БД.

    Args:
        key: ключ
    """
    if transaction_stack:
        current_transaction = transaction_stack[-1]
        if key in current_transaction["changes"]:
            del current_transaction["changes"][key]
        current_transaction["deleted"].add(key)
    else:
        values.pop(key, None)


def get_value(key: str) -> str:
    """Получение значения по ключу.

    Args:
        key: ключ

    Returns:
        str: значение. NULL, если значение не найдено
    """
    for transaction in reversed(transaction_stack):
        if key in transaction["deleted"]:
            return "NULL"
        if key in transaction["changes"]:
            return transaction["changes"][key]

    if key in values:
        return values[key]
    else:
        return "NULL"


def counts_value(value: str) -> int:
    """Подсчет количества значений в БД.

    Args:
        value: значение

    Returns:
        int: количество значений
    """
    temp_values = get_current_state(values, transaction_stack)

    return list(temp_values.values()).count(value)


def find_keys(target_value: str) -> str:
    """Поиск ключей по значению.

    Args:
        target_value: значение

    Returns:
        str: ключи. NULL, если ключ не найден
    """
    temp_values = get_current_state(values, transaction_stack)
    matching_keys = [k for k, v in temp_values.items() if v == target_value]

    if not matching_keys:
        return "NULL"
    return " ".join(matching_keys)


def begin() -> None:
    """Начало новой транзакции."""
    transaction_stack.append({"changes": {}, "deleted": set()})


def rollback() -> str | None:
    """Откат текущей транзакции."""
    if not transaction_stack:
        return "NO TRANSACTION"

    transaction_stack.pop()


def commit() -> str | None:
    """Фиксация изменений текущей (самой внутренней) транзакции."""
    if not transaction_stack:
        return "NO TRANSACTION"

    transaction = transaction_stack.pop()

    if transaction_stack:
        parent = transaction_stack[-1]

        for key in transaction["deleted"]:
            parent["deleted"].add(key)
            parent["changes"].pop(key, None)

        parent["changes"].update(transaction["changes"])
    else:
        for key in transaction["deleted"]:
            values.pop(key, None)
        values.update(transaction["changes"])


commands = {
    "get": get_value,
    "set": set_value,
    "counts": counts_value,
    "unset": unset_value,
    "find": find_keys,
    "begin": begin,
    "rollback": rollback,
    "commit": commit,
}
