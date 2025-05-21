import json


from src.reports import spending_by_category
from src.services import simple_search
from src.utils import load_transactions
from src.views import home_page


def main() -> None:
    """Главная точка входа в приложение."""
    try:
        # пример использования
        print("Home Page Data:")
        home_data = home_page("2021-12-31 16:00:00")
        print(json.dumps(home_data, indent=2, ensure_ascii=False))

        # загрузка всех транзакций
        transactions = load_transactions()

        print("\nРезультат поиска:")
        search_results = simple_search("Магнит", transactions)
        print(json.dumps(search_results, indent=2, ensure_ascii=False, default=str))

        print("\nОтчет по расходам по категориям:")
        spending_report = spending_by_category(transactions, "Супермаркеты", "2021-12-31")
        print(json.dumps(spending_report, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
