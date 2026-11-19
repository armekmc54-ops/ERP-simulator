import unittest
from rules import classify_invoice


class MatchTests(unittest.TestCase):
    def base(self, **changes):
        row = dict(active=True, ordered=10, received=10, invoiced=10,
                   order_price=5000, invoice_price=5000, has_receipt=True)
        return row | changes

    def test_matching_invoice(self):
        self.assertEqual(classify_invoice(self.base()), 'APPROVED')

    def test_partial_receipt_and_invoice(self):
        self.assertEqual(classify_invoice(self.base(received=4, invoiced=4)), 'APPROVED')

    def test_excess_quantity(self):
        self.assertEqual(classify_invoice(self.base(invoiced=11)), 'QUANTITY_MISMATCH')

    def test_price_difference(self):
        self.assertEqual(classify_invoice(self.base(invoice_price=5500)), 'PRICE_MISMATCH')

    def test_missing_receipt(self):
        self.assertEqual(classify_invoice(self.base(has_receipt=False)), 'MISSING_RECEIPT')

    def test_blocked_supplier(self):
        self.assertEqual(classify_invoice(self.base(active=False)), 'INACTIVE_SUPPLIER')

    def test_negative_or_zero_quantity(self):
        self.assertEqual(classify_invoice(self.base(invoiced=0)), 'INVALID_VALUES')
        self.assertEqual(classify_invoice(self.base(order_price=-1)), 'INVALID_VALUES')


if __name__ == '__main__':
    unittest.main()
