import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_PATH = os.path.join(
    BASE_DIR,
    'data',
    'news.json'
)

def ensure_json_exists():
    os.makedirs(
        os.path.dirname(JSON_PATH),
        exist_ok=True
    )

    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_news():
    ensure_json_exists()

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_news(news_list):
    ensure_json_exists()

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(
            news_list,
            f,
            ensure_ascii=False,
            indent=2
        )