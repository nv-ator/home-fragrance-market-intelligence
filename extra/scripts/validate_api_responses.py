import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

res = client.get('/api/overview').json()
print('Overview total_products:', res['total_products'])
print('Overview avg_selling_price:', res['avg_selling_price'])
print('Overview median_selling_price:', res['median_selling_price'])
print('Overview avg_rating:', res['avg_rating'])
print('Overview total_reviews:', res['total_reviews'])
print('Overview avg_discount_pct:', res['avg_discount_pct'])
print('Overview discounted_products:', res['discounted_products'])

res_pp = client.get('/api/analytics/price-positioning').json()
print('PP price_distribution:', res_pp['price_distribution'])
print('PP summary:', res_pp['price_summary'])

res_pn = client.get('/api/analytics/price-normalization').json()
for fmt in ['liquid_ml', 'solid_g']:
    f = res_pn[fmt]
    print(fmt, 'count:', f['count'], 'avg:', f['avg_price_per_unit'], 'median:', f['median_price_per_unit'], 'min:', f['min_price_per_unit'], 'max:', f['max_price_per_unit'])

res_disc = client.get('/api/analytics/discounts').json()
print('Discounts total_discounted:', res_disc['total_discounted_products'])
print('Discounts avg_discount:', res_disc['avg_discount_pct'])

res_ins = client.get('/api/insights').json()
print('Insights count:', len(res_ins))
for ins in res_ins:
    print('Insight:', ins['id'], '->', ins['title'])
