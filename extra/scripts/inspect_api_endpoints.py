from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

endpoints = [
    '/api/overview',
    '/api/brands/comparison',
    '/api/analytics/price-positioning',
    '/api/analytics/price-normalization',
    '/api/analytics/categories',
    '/api/analytics/platforms',
    '/api/analytics/discounts',
    '/api/analytics/category-coverage',
    '/api/insights'
]

for ep in endpoints:
    res = client.get(ep)
    print(f'=== {ep} === (Status: {res.status_code})')
    data = res.json()
    if isinstance(data, list):
        print(f'  List len: {len(data)}')
        if len(data) > 0:
            print(f'  First item: {data[0]}')
    elif isinstance(data, dict):
        print('  Keys:', list(data.keys()))
        for k in list(data.keys())[:5]:
            print(f'    {k}: {str(data[k])[:80]}')
