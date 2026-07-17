import unittest
from unittest.mock import   patch, mock_open, MagicMock
from menu_manager import MenuManager
from exeptions import InsuffincientSharesError
import database

class TestDatabase(unittest.TestCase):

    @patch("database.os.path.isfile")
    def test_load_stock_market_success(self, mock_isfile):
        # 1. Przygotowanie mocka
        mock_isfile.return_value = True
        fake_json_content = '{"PKO.WA": {"name": "PKO BP", "price": 100.0}}'
        
        # 2. Uzycie mock_open, aby udawać zawartość pliku
        with patch("builtins.open", mock_open(read_data=fake_json_content)):
            result = database.load_stock_market()

        # 3. Weryfikacja
        self.assertIn("PKO.WA", result)
        self.assertEqual(result["PKO.WA"].price, 100.0)


    @patch("database.os.path.isfile")
    def test_load_stock_market_file_not_found(self, mock_isfile):
        # Symulujemy brak pliku
        mock_isfile.return_value = False

        result = database.load_stock_market()

        self.assertEqual(result, {})

class TestMenuManager(unittest.TestCase):
    def setUp(self):
        # Przygotowanie "zaślepek" (mocki) dla zaleznośći
        self.mock_wallet = MagicMock()
        self.mock_market = {"PKO.WA": MagicMock(ticker="PKO.WA")}
        self.menu = MenuManager(self.mock_wallet, self.mock_market, {})

    @patch("menu_manager.Prompt.ask")
    @patch("menu_manager.save_transaction_history")
    def test_handle_sell_success(self, mock_save, mock_prompt):
        # 1. Ustawiamy zachowanie mocków
        mock_prompt.side_effect = ["PKO.WA", "5"] # Symuluje wpisanie tickera i ilości
        self.mock_wallet.sell.return_value = ("Sprzedano akcje", MagicMock())

        # 2. Wywołanie metody
        result = self.menu.handle_sell()

        # 3. Weryfikacja czy zadziałało
        self.assertEqual(result, "Sprzedano akcje")
        self.mock_wallet.sell.assert_called_once()
        mock_save.assert_called_once()

    @patch("menu_manager.Prompt.ask")
    def test_handle_sell_insufficient_shares(self, mock_prompt):
        # Symulacja błędu brak wystarczajacej liczby akcji
        mock_prompt.side_effect = ["PKO.WA", "5"]
        self.mock_wallet.sell.side_effect = InsuffincientSharesError("Brak akcji")

        # Poniewaz w handle_sell jest pętla while i continue,
        # trzeba przerwać test, podając zły input w drugim przebiegu
        # lub uzyć wywołania, które zakończy pętlę.
        # Teraz sprawdźmy tylko czy metoda obsługuje wyjątek

        with patch("menu_manager.Prompt.ask", side_effect=["PKO.WA", "5", "b"]):
            # Tutaj trzeba dodać wyjście z pętli, zeby test się nie zawiesił
            pass
        

if __name__ == '__main__':
    unittest.main()
