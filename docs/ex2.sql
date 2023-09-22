SELECT
    t.client_id,
    SUM(IF(p.product_type='MEUBLE', t.prod_price * t.prod_qty, 0)) as ventes_meuble,
    SUM(IF(p.product_type='DECO', t.prod_price * t.prod_qty, 0)) as ventes_deco
FROM TRANSACTION t JOIN PRODUCT_NOMENCLATURE p ON t.prod_id = p.product_id
WHERE STR_TO_DATE(date, '%d/%m/%Y') BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY t.client_id;