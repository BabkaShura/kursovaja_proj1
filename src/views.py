import logging
from datetime import datetime
from typing import Any
from typing import Dict

from . import services
from . import utils


def home_page(date_time: str) -> Dict[str, Any]:
    """
    Generate home page JSON response with financial data.

    Args:
        date_time: String in format 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Dictionary containing greeting, cards info, top transactions,
        currency rates and stock prices
    """
    try:
        # Parse input date
        input_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        # Get greeting based on time
        greeting = utils.get_greeting(input_date)

        # Load transactions for the month
        transactions = utils.load_transactions_for_month(input_date)
        transactions = transactions.fillna("").astype(str)

        # Process cards data
        cards = services.process_cards_data(transactions)

        # Get top 5 transactions
        top_transactions = services.get_top_transactions(transactions, 5)

        # Get currency rates
        currency_rates = utils.get_currency_rates()

        # Get stock prices
        stock_prices = utils.get_stock_prices()

        return {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

    except Exception as e:
        logging.error(f"Error in home_page: {str(e)}")
        raise
