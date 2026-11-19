"""Independent reference for the single-item AP teaching example (MXN cents)."""


def classify_invoice(row):
    if not row['active']:
        return 'INACTIVE_SUPPLIER'
    if not row['has_receipt']:
        return 'MISSING_RECEIPT'
    if (min(row['ordered'], row['received'], row['invoiced']) <= 0
            or min(row['order_price'], row['invoice_price']) < 0):
        return 'INVALID_VALUES'
    if row['received'] > row['ordered'] or row['invoiced'] > row['received']:
        return 'QUANTITY_MISMATCH'
    if row['order_price'] != row['invoice_price']:
        return 'PRICE_MISMATCH'
    return 'APPROVED'
