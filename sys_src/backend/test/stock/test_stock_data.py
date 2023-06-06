import unittest
import os

from sys_src.backend.src.stock import stock_data


class TestStockData(unittest.TestCase):
    def test_get_data(self):
        stock_symbol = "MSF.DE"
        path = "../data/" + stock_symbol + ".json"
        stock_data.get_data(stock_symbol, path)

        self.assertTrue(os.path.exists(path))

        stock_symbol = "MSFT"
        path = "../data/" + stock_symbol + ".json"
        stock_data.get_data(stock_symbol, path)

        self.assertTrue(os.path.exists(path))

    def test_is_dat_updated(self):
        stock_symbol = "MSF.DE"
        path = "../data/" + stock_symbol + ".json"

        self.assertTrue(stock_data.is_data_updated(path))

        stock_symbol = "APPL"
        path = "../data/" + stock_symbol + ".json"

        self.assertFalse(stock_data.is_data_updated(path))
