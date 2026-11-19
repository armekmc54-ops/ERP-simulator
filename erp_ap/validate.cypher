MATCH (s:APDemo:Supplier)-[:SUPPLIES]->(o:APDemo:PurchaseOrder)<-[:BILLS]-(i:APDemo:Invoice)
OPTIONAL MATCH (i)-[:BASED_ON]->(r:APDemo:Receipt)-[:RECEIVES]->(o)
WITH s, o, i, r,
CASE
 WHEN NOT s.active THEN 'INACTIVE_SUPPLIER'
 WHEN r IS NULL THEN 'MISSING_RECEIPT'
 WHEN o.quantity <= 0 OR r.quantity <= 0 OR i.quantity <= 0
      OR o.unit_price_cents < 0 OR i.unit_price_cents < 0 THEN 'INVALID_VALUES'
 WHEN r.quantity > o.quantity OR i.quantity > r.quantity THEN 'QUANTITY_MISMATCH'
 WHEN o.unit_price_cents <> i.unit_price_cents THEN 'PRICE_MISMATCH'
 ELSE 'APPROVED'
END AS decision
RETURN i.id AS invoice, o.id AS purchase_order, r.id AS receipt,
       decision, decision = 'APPROVED' AS payment_allowed,
       i.quantity * i.unit_price_cents AS amount_cents
ORDER BY invoice;
