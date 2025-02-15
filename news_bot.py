import os
import requests
from datetime import datetime, timedelta

# Load API keys from environment variables
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Define search parameters
KEYWORDS = ["trump", "elon musk"]
# For example, filter articles from the last day
today = datetime.utcnow()
from_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

def fetch_articles():
    url = "https://newsapi.org/v2/everything"
    query = " OR ".join(KEYWORDS)
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
        "language": "en",
        "pageSize": 5  # Adjust as needed
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print("Error fetching articles:", response.text)
        return []

def send_to_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(telegram_url, data=payload)
    if response.status_code != 200:
        print("Error sending message:", response.text)

def main():
    articles = fetch_articles()
    if not articles:
        send_to_telegram("No new articles found.")
        return

    for article in articles:
        # You can add more sophisticated filtering (e.g., sentiment analysis) here.
        title = article.get("title")
        url = article.get("url")
        published_at = article.get("publishedAt")
        message = f"*{title}*\nPublished: {published_at}\n[Read more]({url})"
        send_to_telegram(message)

if __name__ == "__main__":
    main()