SELECT
    date,
    SUM(prod_price * prod_qty) as ventes
FROM TRANSACTION
WHERE STR_TO_DATE(date, '%d/%m/%Y') between "01-01-2019" and "31-12-2019"
GROUP BY  date
ORDER BY date ASC
