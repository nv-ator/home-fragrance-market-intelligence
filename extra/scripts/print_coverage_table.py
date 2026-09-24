import sqlite3
import pandas as pd

conn = sqlite3.connect('data/market_intelligence.db')
cursor = conn.cursor()

cats = [r[0] for r in cursor.execute('SELECT category_name FROM categories ORDER BY category_name;').fetchall()]
brands = [r[0] for r in cursor.execute('SELECT brand_name FROM brands ORDER BY brand_name;').fetchall()]

header = f'{"Category":<32} | ' + ' | '.join([f'{b:<10}' for b in brands]) + ' | Total'
print(header)
print('-' * len(header))
for cat in cats:
    counts = []
    tot = 0
    for b in brands:
        c = cursor.execute('''
            SELECT COUNT(p.product_id) 
            FROM products p 
            JOIN brands br ON p.brand_id = br.brand_id 
            JOIN categories ca ON p.category_id = ca.category_id 
            WHERE ca.category_name = ? AND br.brand_name = ?;
        ''', (cat, b)).fetchone()[0]
        counts.append(c)
        tot += c
    row_str = f'{cat:<32} | ' + ' | '.join([f'{c:<10}' for c in counts]) + f' | {tot}'
    print(row_str)

# Total row
col_totals = []
grand_total = 0
for b in brands:
    c = cursor.execute('''
        SELECT COUNT(p.product_id) 
        FROM products p 
        JOIN brands br ON p.brand_id = br.brand_id 
        WHERE br.brand_name = ?;
    ''', (b,)).fetchone()[0]
    col_totals.append(c)
    grand_total += c
print('-' * len(header))
tot_str = f'{"Total":<32} | ' + ' | '.join([f'{c:<10}' for c in col_totals]) + f' | {grand_total}'
print(tot_str)
