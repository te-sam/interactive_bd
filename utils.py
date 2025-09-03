"""Модуль для вспомогательных функций."""


def get_current_state(values, transaction_stack) -> dict[str, str]:
    """Получение текущего состояния БД.

    Args:
        values: словарь значений
        transaction_stack: стек транзакций

    Returns:
        dict[str, str]: текущий состояние
    """
    temp_values = values.copy()

    for transaction in transaction_stack:
        for key in transaction["deleted"]:
            if key in temp_values:
                del temp_values[key]
        temp_values.update(transaction["changes"])
    return temp_values
