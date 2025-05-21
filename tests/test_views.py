from typing import Any
from typing import Dict
from typing import List
from typing import cast
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.utils import load_transactions
from src.views import home_page


@pytest.fixture
def mock_transactions() -> List[Dict[str, Any]]:
    return cast(List[Dict[str, Any]], load_transactions())


@patch("src.utils.get_greeting")
@patch("src.utils.load_transactions_for_month")
@patch("src.utils.get_currency_rates")
@patch("src.utils.get_stock_prices")
def test_home_page(
    mock_stocks: MagicMock,
    mock_rates: MagicMock,
    mock_trans: MagicMock,
    mock_greet: MagicMock,
    mock_transactions: List[Dict[str, Any]],
) -> None:
    mock_greet.return_value = "Добрый день"
    mock_trans.return_value = mock_transactions
    mock_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = home_page("2021-12-31 16:00:00")

    assert result["greeting"] == "Добрый день"
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)
