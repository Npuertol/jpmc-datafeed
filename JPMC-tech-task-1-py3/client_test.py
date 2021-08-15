import unittest
from client3 import getDataPoint
from client3 import getRatio


class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
                'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
             'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        """ ------------ Add the assertion below ------------ """
        for quote in quotes:
            test = getDataPoint(quote)
            quoteprice = ((quote['top_bid']['price']) +
                          (quote['top_ask']['price'])) / 2
            self.assertEqual(test[0], quote['stock'])
            self.assertEqual(test[1], (quote['top_bid']['price']))
            self.assertEqual(test[2], (quote['top_ask']['price']))
            self.assertEqual(test[3], quoteprice)

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
                'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
        ]
        """ ------------ Add the assertion below ------------ """
        for quote in quotes:
            test = getDataPoint(quote)
            quoteprice = ((quote['top_bid']['price']) +
                          (quote['top_ask']['price'])) / 2
            self.assertEqual(test[0], quote['stock'])
            self.assertEqual(test[1], (quote['top_bid']['price']))
            self.assertEqual(test[2], (quote['top_ask']['price']))
            self.assertEqual(test[3], quoteprice)

    """ ------------ Add more unit tests ------------ """
    # unit test for getRatio for cases when price_a = 0 or price_b = 0

    def test_getRatio_priceBzero(self):
      # changed 'ABC' to have ask and bid of 0, resulting in price of 0
        quotes = [{'top_ask': {'price': 0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
                   'top_bid': {'price': 0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
                  {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453',
                   'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}]
        prices = {}
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price
        # if price_b = 0
        self.assertEqual(getRatio(prices['DEF'], prices['ABC']), None)
        # if price_a = 0
        self.assertEqual(getRatio(prices['ABC'], prices['DEF']), 0)


if __name__ == '__main__':
    unittest.main()
