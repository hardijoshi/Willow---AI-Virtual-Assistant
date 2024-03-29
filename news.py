import random
from newsapi import NewsApiClient
# Init
newsapi = NewsApiClient(api_key='cc7fcf60d59944aaa8984902b3e1030b')

def get_top_headlines(category):
    top_headlines = newsapi.get_top_headlines(
        category=category,
        language='en',
        country='in')

    if top_headlines['status'] == 'ok':
        return top_headlines['articles']
    else:
        print("Failed to fetch top headlines for", category, ":", top_headlines['message'])
        return []

def get_random_news(articles, count=3):
    return random.sample(articles, min(count, len(articles)))

def print_news(article):
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']['name']}")
    print()

def main():
    categories = ['general', 'sports', 'entertainment', 'health', 'business']
    
    for category in categories:
        print(f"Top headlines in {category}:")
        articles = get_top_headlines(category)
        if articles:
            random_articles = get_random_news(articles)
            for article in random_articles:
                print_news(article)
        print()

if __name__ == "__main__":
    main()
