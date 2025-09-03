"""Основной модуль.

Предоставляет функции для запуска команд и работы с БД.
"""

from commands import commands


def run_command(command: str, *args) -> None:
    """Запуск команды.

    Args:
        command: команда
        *args: аргументы
    """
    command = command.lower()

    if command == "end":
        raise SystemExit

    if command not in commands:
        print("UNKNOWN COMMAND")
        return

    result = commands[command](*args)
    if result is not None:
        print(result)


def main() -> None:
    """Основная функция."""
    while True:
        request = input("> ").strip().split()
        if not request:
            continue
        try:
            run_command(*request)
        except SystemExit:
            break
        except Exception:
            print("WRONG REQUEST")


if __name__ == "__main__":
    main()
