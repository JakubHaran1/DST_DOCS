from typing import List, Union

class Calendar_dst:
    """
    Klasa reprezentująca kalendarz.

    Parameters:
    year (int): Rok.
    month (int): Miesiąc.
    day (int): Dzień.
    work_days (List[str]): Lista dni roboczych.
    full_days (List[str]): Lista dni pełnych.

    Attributes:
    year (int): Rok.
    month (int): Miesiąc.
    day (int): Dzień.
    work_days (List[str]): Lista dni roboczych.
    full_days (List[str]): Lista dni pełnych.
    leap (bool): Informacja czy rok jest przestępny.
    days (int): Liczba dni w miesiącu.

    Methods:
    is_leap(year: int) -> bool: Sprawdza czy rok jest przestępny.
    get_days(month: int, leap: bool) -> int: Zwraca liczbę dni w miesiącu.
    print_calendar(days: int, month: int, year: int) -> None: Wyświetla kalendarz.

    """

    def __init__(self, year: int, month: int, day: int, work_days: List[str], full_days: List[str]) -> None:
        """
        Inicjalizuje kalendarz.

        Args:
        year (int): Rok.
        month (int): Miesiąc.
        day (int): Dzień.
        work_days (List[str]): Lista dni roboczych.
        full_days (List[str]): Lista dni pełnych.
        """

    def is_leap(self, year: int) -> bool:
        """
        Sprawdza czy rok jest przestępny.

        Args:
        year (int): Rok.

        Returns:
        bool: True jeśli rok jest przestępny, False w przeciwnym przypadku.
        """

    def get_days(self, month: int, leap: bool) -> int:
        """
        Zwraca liczbę dni w miesiącu.

        Args:
        month (int): Miesiąc.
        leap (bool): Informacja czy rok jest przestępny.

        Returns:
        int: Liczba dni w miesiącu.
        """

    def print_calendar(self, days: int, month: int, year: int) -> None:
        """
        Wyświetla kalendarz.

        Args:
        days (int): Liczba dni w miesiącu.
        month (int): Miesiąc.
        year (int): Rok.
        """
