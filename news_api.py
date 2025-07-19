# news_api.py
import requests
import os
from datetime import datetime, timedelta

# NEWS_API_KEY = os.getenv("NEWS_API_KEY") # Recommended: Load from environment variable

# For simplicity in this example, directly set it.
# Replace "YOUR_NEWSAPI_KEY" with your actual NewsAPI key
NEWS_API_KEY = "2791cfb2c1d6497c901dc1442fa4db2e" # <<< IMPORTANT: Replace with your actual NewsAPI key or use os.getenv()

def get_top_headlines(country='us', category=None, query=None, page_size=5):
    """
    Fetches top news headlines from NewsAPI.org.

    Args:
        country (str): The 2-letter ISO 3166-1 code of the country you want to get headlines for.
                       (e.g., 'us', 'in', 'gb')
        category (str): The category you want to get headlines for. (e.g., 'business', 'entertainment', 'health', 'science', 'sports', 'technology')
        query (str): Keywords or phrases to search for in the article title and content.
        page_size (int): The number of results to return per page (max 100).

    Returns:
        A list of dictionaries, each representing a news article, or None if an error occurs.
    """
    if not NEWS_API_KEY:
        print("❌ Error: NEWS_API_KEY not set. Cannot fetch news.")
        return None

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': NEWS_API_KEY,
        'pageSize': page_size
    }
    if country:
        params['country'] = country
    if category:
        params['category'] = category
    if query:
        params['q'] = query

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        articles = data.get('articles', [])
        return articles
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching news: {e}")
        return None

def format_articles_for_gemini(articles):
    """
    Formats a list of news articles into a string suitable for Gemini summarization.
    """
    if not articles:
        return "No news articles found."

    formatted_text = "Here are some recent news headlines:\n"
    for i, article in enumerate(articles):
        title = article.get('title', 'No title')
        source = article.get('source', {}).get('name', 'Unknown source')
        formatted_text += f"{i+1}. From {source}: {title}\n"
    return formatted_text 