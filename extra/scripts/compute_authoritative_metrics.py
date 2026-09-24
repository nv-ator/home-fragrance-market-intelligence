import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('data/market_intelligence.db')
df = pd.read_sql_query('SELECT * FROM vw_products_analytical', conn)

print('=== TOTAL PRODUCTS ===')
print('Count:', len(df))

print('\n=== BRAND COUNTS ===')
bc = df['brand'].value_counts()
print(bc)
print('Brand percentages:\n', (bc / len(df) * 100).round(2))

print('\n=== PLATFORM COUNTS ===')
pc = df['platform'].value_counts()
print(pc)
print('Platform percentages:\n', (pc / len(df) * 100).round(2))

print('\n=== CATEGORY COUNTS ===')
cc = df['category'].value_counts()
print(cc)
print('Category percentages:\n', (cc / len(df) * 100).round(2))

print('\n=== MARKET METRICS ===')
print('Selling Price Mean:', round(df['selling_price'].mean(), 2))
print('Selling Price Median:', round(df['selling_price'].median(), 2))
print('Selling Price Min:', df['selling_price'].min(), 'Max:', df['selling_price'].max())
print('Selling Price Std Dev:', round(df['selling_price'].std(), 2))

rated_df = df[df['rating'].notnull()]
print('Rated Count:', len(rated_df), f'({round(len(rated_df)/len(df)*100, 2)}%)')
print('Rating Mean:', round(rated_df['rating'].mean(), 2))
print('Rating Median:', round(rated_df['rating'].median(), 2))
print('Rating Min:', rated_df['rating'].min(), 'Max:', rated_df['rating'].max())

rev_df = df[df['review_count'].notnull()]
print('Review Count Present Items:', len(rev_df))
print('Total Review Count Sum:', int(rev_df['review_count'].sum()))
print('Review Mean (of present):', round(rev_df['review_count'].mean(), 2))
print('Review Median (of present):', round(rev_df['review_count'].median(), 2))

disc_df = df[df['discount_pct'].notnull() & (df['discount_pct'] > 0)]
print('Discounted Products (>0%):', len(disc_df), f'({round(len(disc_df)/len(df)*100, 2)}%)')
print('Discount Pct Mean (>0%):', round(disc_df['discount_pct'].mean(), 2))
print('Discount Pct Median (>0%):', round(disc_df['discount_pct'].median(), 2))
print('Discount Pct Min:', disc_df['discount_pct'].min(), 'Max:', disc_df['discount_pct'].max())

all_disc_df = df[df['discount_pct'].notnull()]
print('All Discount Pct non-null Count:', len(all_disc_df))

print('\n=== BRAND SPECIFIC METRICS ===')
for brand in sorted(df['brand'].unique()):
    b_df = df[df['brand'] == brand]
    b_rated = b_df[b_df['rating'].notnull()]
    b_rev = b_df[b_df['review_count'].notnull()]
    b_disc = b_df[b_df['discount_pct'].notnull() & (b_df['discount_pct'] > 0)]
    print(f'Brand: {brand}')
    print(f'  Product Count: {len(b_df)} ({round(len(b_df)/len(df)*100, 2)}%)')
    p_mean = round(b_df['selling_price'].mean(), 2)
    p_med = round(b_df['selling_price'].median(), 2)
    print(f'  Price Mean: {p_mean}, Median: {p_med}, Min: {b_df["selling_price"].min()}, Max: {b_df["selling_price"].max()}')
    r_count = len(b_rated)
    r_mean = round(b_rated['rating'].mean(), 2) if len(b_rated) > 0 else 'None'
    r_med = round(b_rated['rating'].median(), 2) if len(b_rated) > 0 else 'None'
    print(f'  Rated Count: {r_count} ({round(r_count/len(b_df)*100, 2)}%), Rating Mean: {r_mean}, Median: {r_med}')
    rev_sum = int(b_rev['review_count'].sum()) if len(b_rev) > 0 else 0
    print(f'  Review Sum: {rev_sum} (Present items: {len(b_rev)})')
    d_count = len(b_disc)
    d_mean = round(b_disc['discount_pct'].mean(), 2) if len(b_disc) > 0 else 'None'
    d_med = round(b_disc['discount_pct'].median(), 2) if len(b_disc) > 0 else 'None'
    print(f'  Discount Count (>0): {d_count} ({round(d_count/len(b_df)*100, 2)}%), Discount Mean (>0): {d_mean}%, Median: {d_med}%')
    print(f'  Categories ({b_df["category"].nunique()}): {dict(b_df["category"].value_counts())}')
    print(f'  Platforms ({b_df["platform"].nunique()}): {dict(b_df["platform"].value_counts())}')

print('\n=== PRICE DISTRIBUTION ===')
u250 = len(df[df['selling_price'] < 250])
b250_499 = len(df[(df['selling_price'] >= 250) & (df['selling_price'] < 500)])
b500_999 = len(df[(df['selling_price'] >= 500) & (df['selling_price'] < 1000)])
b1000_1999 = len(df[(df['selling_price'] >= 1000) & (df['selling_price'] < 2000)])
b2000_plus = len(df[df['selling_price'] >= 2000])
print(f'Under ₹250 (< 250): {u250} ({round(u250/len(df)*100, 2)}%)')
print(f'₹250–₹499 (250 <= price < 500): {b250_499} ({round(b250_499/len(df)*100, 2)}%)')
print(f'Total under ₹500: {u250 + b250_499} ({round((u250+b250_499)/len(df)*100, 2)}%)')
print(f'₹500–₹999 (500 <= price < 1000): {b500_999} ({round(b500_999/len(df)*100, 2)}%)')
print(f'₹1,000–₹1,999 (1000 <= price < 2000): {b1000_1999} ({round(b1000_1999/len(df)*100, 2)}%)')
print(f'₹2,000+ (price >= 2000): {b2000_plus} ({round(b2000_plus/len(df)*100, 2)}%)')

print('\n=== UNIT ECONOMICS ===')
ml_df = df[df['price_per_100ml'].notnull()]
print(f'₹/100ml count: {len(ml_df)}, Mean: {round(ml_df["price_per_100ml"].mean(), 2)}, Median: {round(ml_df["price_per_100ml"].median(), 2)}, Min: {ml_df["price_per_100ml"].min()}, Max: {ml_df["price_per_100ml"].max()}')
g_df = df[df['price_per_100g'].notnull()]
print(f'₹/100g count: {len(g_df)}, Mean: {round(g_df["price_per_100g"].mean(), 2)}, Median: {round(g_df["price_per_100g"].median(), 2)}, Min: {g_df["price_per_100g"].min()}, Max: {g_df["price_per_100g"].max()}')

print('\n=== PRICE VS RATING ===')
pr_df = df[df['selling_price'].notnull() & df['rating'].notnull()]
print('Rated product count:', len(pr_df))
r = pr_df['selling_price'].corr(pr_df['rating'])
print('Pearson correlation (price vs rating):', round(r, 4))
