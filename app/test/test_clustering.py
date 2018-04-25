import unittest
from app.src import clustering


class AggregationTest(unittest.TestCase):

    def test_purity_calculation(self):
        a = {'a': 10, 'b': 1, 'c': 5}
        b = {'a': 5, 'b': 10, 'c': 1}
        c = {'a': 1, 'b': 5, 'c': 10}

        d = {'C1': a, 'C2': b, 'C3': c}

        purity = clustering.calculate_purity_score(d, 48)
        self.assertEquals(0.625, purity)
