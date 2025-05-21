import json
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import get_currency_rates
from src.utils import get_stock_prices

mock_settings = {"user_currencies": ["USD", "EUR", "GBP"], "user_stocks": ["AAPL", "GOOGL", "TSLA"]}


@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_settings))
@patch("src.utils.os.getenv", return_value="dummy_api_key")
def test_get_currency_rates(mock_getenv: MagicMock, mock_file: MagicMock) -> None:
    rates = get_currency_rates()
    assert isinstance(rates, list)
    assert {"currency": "USD", "rate": 75.0} in rates
    assert {"currency": "EUR", "rate": 85.0} in rates
    assert {"currency": "GBP", "rate": 0} in rates  # Mock does not include GBP


@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_settings))
@patch("src.utils.os.getenv", return_value="dummy_api_key")
def test_get_stock_prices(mock_getenv: MagicMock, mock_file: MagicMock) -> None:
    prices = get_stock_prices()
    assert isinstance(prices, list)
    assert {"stock": "AAPL", "price": 150.0} in prices
    assert {"stock": "GOOGL", "price": 2750.0} in prices
    assert {"stock": "TSLA", "price": 1000.0} in prices
