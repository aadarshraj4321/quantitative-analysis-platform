from tools.news_tools import get_combined_news_and_sentiment_debug

def test_news():
    ticker = "RELIANCE.NS"
    company_name = "Reliance Industries"
    
    print(f"Testing news scraping for {ticker} ({company_name})")
    result = get_combined_news_and_sentiment_debug(ticker, company_name)
    
    print(f"\nResults:")
    print(f"Total articles: {result['sentiment_summary']['total_items']}")
    print(f"Positive: {result['sentiment_summary']['positive']}")
    print(f"Negative: {result['sentiment_summary']['negative']}")
    print(f"Neutral: {result['sentiment_summary']['neutral']}")
    
    if result['articles']:
        print(f"\nSample articles:")
        for i, article in enumerate(result['articles'][:3]):
            print(f"{i+1}. {article['title']}")
            print(f"   Source: {article['source']} | Sentiment: {article['sentiment']}")

if __name__ == "__main__":
    test_news()