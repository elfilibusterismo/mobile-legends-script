import json
from google_play_scraper import app, reviews, Sort
from datetime import datetime

def convert_datetime(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')

app_details = app('com.elfilibustero.origin')

reviews_data, _ = reviews(
    'com.elfilibustero.origin',
    lang='en',
    country='us',
    sort=Sort.NEWEST,
    count=5
)

combined_data = {
    "app_details": app_details,
    "reviews": reviews_data,
    "generated_at": datetime.now().isoformat()
}

with open('data/app_data.json', 'w') as json_file:
    json.dump(combined_data, json_file, indent=2, default=convert_datetime)
