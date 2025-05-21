import re

import pandas as pd
import pytest

from src.services import phone_search
from src.services import simple_search
from src.utils import load_transactions


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    return load_transactions()


def test_simple_search(sample_transactions: pd.DataFrame) -> None:
    results = simple_search("Магнит", sample_transactions)
    assert isinstance(results, list)
    if results:  # If there are matching transactions
        assert "Магнит" in results[0]["description"]


def test_phone_search(sample_transactions: pd.DataFrame) -> None:
    results = phone_search(sample_transactions)
    assert isinstance(results, list)
    if results:  # If there are phone numbers
        assert re.search(r"(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}", results[0]["description"])
