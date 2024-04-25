
import json
import jmespath
import pandas as pd

'''
'url': '',
'url_prefix': "",
'base_url': '',
'base_format_id': '',
'''
ss={
    "detail_name": "Product 2",
    "produced_at": "2024-04-25",
    "price": 150,
    "description": "This is product 2"
}
print(jmespath.search("detail_name", ss))