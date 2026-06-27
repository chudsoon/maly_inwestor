import unittest
from models import Wallet, Share, Transaction, InsuffincientSharesError


class TestWallet(unittest.TestCase):

    portoflio = {    "PKO.WA": {
        "name": "PKO BP",
        "price": 10.0
    }}

    def test_buy_sufficient_funds(self):
        # arrange
        wallet = Wallet(1000.0, {}, 0.0, {}, {})
        share = Share('XYZ', 'XYZ CO', 10.0)
        # act 
        result = wallet.buy("id_123", share, 10)

        #sprawdzanie // asset
        # czy gotówka spadła o 100
        self.assertEqual(wallet.cash, 900.0)
        # Czy w portfolio jest 10 akcji XYZ?
        self.assertEqual(wallet.portfolio['XYZ']['quantity'], 10)
        #Czy funkcja zwróciła coś?
        self.assertIn("Zakupiono", result)

    
    def test_insuficient_funds(self):
        # arrange
        wallet = Wallet(5.0, {}, 0.0, {}, {})
        share = Share('PKO.WA', 'PKO BP', 10.0)
        quantity_to_buy = 10
        
        result = wallet.buy("id123", share, quantity_to_buy)

        self.assertEqual(wallet.cash, 5.0)
        self.assertEqual(len(wallet.portfolio), 0)
        self.assertIn("Nie masz wystarczających środków",  result)

    def test_portfolio_updates_after_buy(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {})
        share = Share('XYZ', 'XYZCO', 10.0)

        wallet.buy("id123", share, 1)
        wallet.buy("id1234", share, 1)

        self.assertEqual(len(wallet.portfolio), 1)
        self.assertEqual(wallet.portfolio['XYZ']['quantity'], 2)

    
    def test_sell_shares(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {'XYZ': {'ticker': 'XYZ', 'name': 'XYZCO', 'quantity': 10, 'price': 10.0}})
        share = Share('XYZ', 'XYZCO', 10.0)

    
        result = wallet.sell("id222", share, 4)

        self.assertEqual(wallet.portfolio['XYZ']['quantity'], 6)

        self.assertEqual(wallet.cash, 1040.0)
        self.assertIn("Sprzedano", result)

    def test_oversell(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {'XYZ': {'ticker': 'XYZ', 'name': 'XYZCO', 'quantity': 10, 'price': 10.0}})
        share = Share('XYZ', 'XYZCO', 10.00)
        result = wallet.sell("id123", share, 20)

        self.assertEqual(wallet.cash, 1000.0)
        self.assertEqual(wallet.portfolio['XYZ']['quantity'], 10)
        self.assertIn("Nie masz", result)

    def test_buy_transaction_history(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {'XYZ': {'ticker': 'XYZ', 'name': 'XYZCO', 'quantity': 10, 'price': 10.0}})
        share = Share('XYZ', 'XYZCO', 10.00)

        result = wallet.buy("id123", share, 3)
        self.assertEqual(wallet.cash, 970.0)
        self.assertEqual(len(wallet.transaction_history), 1)

    def test_sell_transcation_history(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {'XYZ': {'ticker': 'XYZ', 'name': 'XYZCO', 'quantity': 10, 'price': 10.0}})
        share = Share('XYZ', 'XYZCO', 10.00)
        result = wallet.sell("id123", share, 3)
        self.assertEqual(wallet.cash, 1030.0)
        self.assertEqual(len(wallet.transaction_history), 1)

    def test_sell_insufficient_shares(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {'XYZ': {'ticker': 'XYZ', 'name': 'XYZCO', 'quantity': 10, 'price': 10.0}})
        share = Share('XYZ', 'XYZCO', 10.00)

        with self.assertRaises(InsuffincientSharesError):
            wallet.sell("id1", share, 10)

    def test_buy_after_market_update(self):
        wallet = Wallet(1000.0, {}, 0.0, {}, {})
        share = Share('XYZ', 'XYZCO', 10.0)
        stock_market = {'XYZ': Share('XYZ', 'XYZCO',8.0)}
        self.assertEqual(wallet.get_shares_value(stock_market), 0.0)
        wallet.buy("id123", share, 1)
        self.assertEqual(wallet.get_shares_value(stock_market), 8.0)
        stock_market['XYZ'].price = 10.0
        self.assertEqual(wallet.get_shares_value(stock_market), 10.0)

        



if __name__ == '__main__':
    unittest.main()


