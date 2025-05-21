import logging
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    рассчитывает расходы по категории за последние 3 месяцв.

    Args:
        transactions: DataFrame с транзакциями
        category: категория для фильтрации
        date: опорная дата в формате 'ГГГГ-ММ-ДД' (по умолчанию используется текущая дата)

    Returns:
        словарь с данными по месяцам для указанной категории
    """
    try:
        if date is None:
            ref_date = datetime.now()
        else:
            ref_date = datetime.strptime(date, "%Y-%m-%d")

        # расчет в период 3 мес
        end_date = ref_date.replace(day=1)
        start_date = (end_date - timedelta(days=1)).replace(day=1)
        start_date = (start_date - timedelta(days=1)).replace(day=1)

        # фильтровка транзакций
        mask = (
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
        )
        filtered = transactions[mask]

        # группировка по месяцам
        result = []
        for month in pd.date_range(start_date, end_date, freq="MS"):
            month_trans = filtered[filtered["Дата операции"].dt.to_period("M") == month.to_period("M")]
            total = month_trans["Сумма операции"].sum()
            result.append({"month": month.strftime("%Y-%m"), "amount": round(float(abs(total)), 2)})

        return {"data": result}
    except Exception as e:
        logging.error(f"Error in spending_by_category: {str(e)}")
        raise
