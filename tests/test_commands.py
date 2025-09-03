"""Модуль тестирования команд."""

from commands import (
    begin,
    commit,
    counts_value,
    find_keys,
    get_value,
    rollback,
    set_value,
    unset_value,
)


def test_set_and_get():
    """Тестирование установки и получения значения."""
    set_value("A", "10")
    assert get_value("A") == "10"


def test_unset():
    """Тестирование удаления значения."""
    set_value("A", "10")
    unset_value("A")
    assert get_value("A") == "NULL"


def test_counts():
    """Тестирование подсчета значений."""
    set_value("A", "10")
    set_value("B", "10")
    set_value("C", "20")
    assert counts_value("10") == 2
    assert counts_value("20") == 1
    assert counts_value("30") == 0


def test_find_keys():
    """Тестирование поиска ключей по значению."""
    set_value("A", "10")
    set_value("B", "10")
    set_value("C", "20")
    assert set(find_keys("10").split()) == {"A", "B"}
    assert find_keys("30") == "NULL"


def test_transactions_commit():
    """Тестирование commit."""
    set_value("A", "10")
    begin()
    set_value("A", "20")
    commit()
    assert get_value("A") == "20"


def test_transactions_rollback():
    """Тестирование rollback."""
    set_value("A", "10")
    begin()
    set_value("A", "20")
    rollback()
    assert get_value("A") == "10"


def test_nested_transactions():
    """Тестирование вложенных транзакций."""
    set_value("A", "10")
    begin()
    set_value("A", "20")
    begin()
    set_value("A", "30")
    rollback()
    assert get_value("A") == "20"
    commit()
    assert get_value("A") == "20"
