UNWIND $rows AS row
MERGE (s:APDemo:Supplier {id: row.id + '-supplier'})
SET s.active = row.active, s.name = 'Proveedor de demostración'
MERGE (o:APDemo:PurchaseOrder {id: row.id + '-order'})
SET o.quantity = row.ordered, o.unit_price_cents = row.order_price, o.item = 'CPU', o.currency = 'MXN'
MERGE (i:APDemo:Invoice {id: row.id})
SET i.quantity = row.invoiced, i.unit_price_cents = row.invoice_price, i.item = 'CPU', i.currency = 'MXN'
MERGE (s)-[:SUPPLIES]->(o)
MERGE (i)-[:BILLS]->(o)
FOREACH (_ IN CASE WHEN row.has_receipt THEN [1] ELSE [] END |
  MERGE (r:APDemo:Receipt {id: row.id + '-receipt'})
  SET r.quantity = row.received, r.item = 'CPU'
  MERGE (r)-[:RECEIVES]->(o)
  MERGE (i)-[:BASED_ON]->(r)
);
