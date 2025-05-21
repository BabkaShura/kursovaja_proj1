import logging
import re
from typing import Any
from typing import Dict
from typing import List
from typing import cast

import pandas as pd


def simple_search(query: str, transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    поиск транзакций по запросу в описании или категории.

    Args:
        query: строка для поиска
        transactions: DataFrame с транзакциями

    Returns:
        список подходящих транзакций с выбранными полями
    """
    try:
        transactions["Описание"] = transactions["Описание"].fillna("").astype(str)
        transactions["Категория"] = transactions["Категория"].fillna("").astype(str)
        mask = transactions["Описание"].str.contains(query, case=False) | transactions["Категория"].str.contains(
            query, case=False
        )
        results = transactions[mask]

        return cast(
            List[Dict[str, Any]],
            results[["Дата операции", "Сумма операции", "Категория", "Описание"]]
            .rename(
                columns={
                    "Дата операции": "date",
                    "Сумма операции": "amount",
                    "Категория": "category",
                    "Описание": "description",
                }
            )
            .to_dict("records"),
        )
    except Exception as e:
        logging.error(f"Error in simple_search: {str(e)}")
        raise


def phone_search(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    функция находит транзакции, содержащие номера телефонов.

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        список транзакций, содержащих номера телефонов
    """
    try:
        transactions["Описание"] = transactions["Описание"].fillna("").astype(str)
        phone_pattern = re.compile(r"(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}")
        mask = transactions["Описание"].apply(lambda x: bool(phone_pattern.search(str(x))))
        results = transactions[mask]

        return cast(
            List[Dict[str, Any]],
            results[["Дата операции", "Сумма операции", "Категория", "Описание"]]
            .rename(
                columns={
                    "Дата операции": "date",
                    "Сумма операции": "amount",
                    "Категория": "category",
                    "Описание": "description",
                }
            )
            .to_dict("records"),
        )
    except Exception as e:
        logging.error(f"Error in phone_search: {str(e)}")
        raise


def process_cards_data(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    функция обрабатывает транзакции для расчета трат по карте и кэшбеку.

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        список словарей по картам с информацией о тратах и кэшбэке
    """
    try:
        # Приводим сумму к числу
        transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce").fillna(0)

        cards_data = []
        for card in transactions["card_last_digits"].unique():
            if pd.isna(card):
                continue

            card_trans = transactions[transactions["card_last_digits"] == card]
            total = card_trans["Сумма операции"].sum()
            cashback = abs(total) // 100

            cards_data.append(
                {
                    "last_digits": card,
                    "total_spent": round(float(abs(total)), 2),
                    "cashback": round(float(cashback), 2),
                }
            )

        return cards_data
    except Exception as e:
        logging.error(f"Error in process_cards_data: {str(e)}")
        raise


def get_top_transactions(transactions: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
    """
    получаем топ N транзакций по сумме

    Args:
        transactions: DataFrame с транзакциями
        n: кол-во транзакций для возврата

    Returns:
        список словарей с топовыми транзакциями
    """
    try:
        # Приводим сумму к числу
        transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce").fillna(0)

        transactions["abs_amount"] = transactions["Сумма операции"].abs()
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

        return cast(
            List[Dict[str, Any]],
            transactions.nlargest(n, "abs_amount")[["Дата операции", "Сумма операции", "Категория", "Описание"]]
            .rename(
                columns={
                    "Дата операции": "date",
                    "Сумма операции": "amount",
                    "Категория": "category",
                    "Описание": "description",
                }
            )
            .assign(date=lambda x: x["date"].dt.strftime("%d.%m.%Y"))
            .to_dict("records"),
        )
    except Exception as e:
        logging.error(f"Error in get_top_transactions: {str(e)}")
        raise
