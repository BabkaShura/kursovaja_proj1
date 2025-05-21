import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pandas as pd
from dotenv import load_dotenv

file_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"
load_dotenv()


def load_transactions() -> pd.DataFrame:
    """загрузка транзакций из xlsx и обработка."""
    try:
        df = pd.read_excel(file_path)

        # преобразование столбцов с датами в формат datatime
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

        # преобразование суммы
        df["Сумма операции"] = df["Сумма операции"].fillna("").astype(str).str.replace(",", ".").astype(float)
        df["Сумма платежа"] = df["Сумма платежа"].fillna("").astype(str).str.replace(",", ".").astype(float)

        # последние 4 цифры номера карты
        df["card_last_digits"] = df["Номер карты"].str.extract(r"\*(\d{4})")

        return df
    except Exception as e:
        logging.error(f"Ошибка при загрузке транзакций: {str(e)}")
        raise


def get_greeting(date_time: datetime) -> str:
    """приветствие в зависимости от времени суток."""
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions_for_month(date_time: datetime) -> pd.DataFrame:
    """загрузка транзакций за месяц, в который входит заданная дата."""
    try:
        df = load_transactions()
        start_date = date_time.replace(day=1)
        mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= date_time)
        return df[mask]
    except Exception as e:
        logging.error(f"Ошибка при загрузке транзакций за месяц: {str(e)}")
        raise


def get_currency_rates() -> List[Dict[str, Any]]:
    """получение текущих курс валют с API."""
    try:
        api_key = os.getenv("CURRENCY_API_KEY")
        settings_path = Path(__file__).resolve().parent.parent / "settings" / "user_settings.json"
        with open(settings_path) as f:
            settings = json.load(f)

        # пример с mock-ответом, потом заменить на реальный
        mock_rates = {"USD": 75.0, "EUR": 85.0}

        return [{"currency": curr, "rate": mock_rates.get(curr, 0)} for curr in settings["user_currencies"]]
    except Exception as e:
        logging.error(f"Ошибка при получении курса валют: {str(e)}")
        raise


def get_stock_prices() -> List[Dict[str, Any]]:
    """получение текущих цен акций с API."""
    try:
        api_key = os.getenv("STOCK_API_KEY")
        settings_path = Path(__file__).resolve().parent.parent / "settings" / "user_settings.json"
        with open(settings_path) as f:
            settings = json.load(f)

        # пример с mock-ответом, потом заменить на реальный
        mock_prices = {"AAPL": 150.0, "AMZN": 3200.0, "GOOGL": 2750.0, "MSFT": 300.0, "TSLA": 1000.0}

        return [{"stock": stock, "price": mock_prices.get(stock, 0)} for stock in settings["user_stocks"]]
    except Exception as e:
        logging.error(f"Ошибка при получении цен акций: {str(e)}")
        raise
