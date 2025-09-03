import yfinance as yf
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import time
import urllib.parse
from typing import List, Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

# --- Model Loading ---
sentiment_pipeline = None
MODEL_PATH = '/code/sentiment_model'

def load_sentiment_pipeline():
    global sentiment_pipeline
    if sentiment_pipeline is None:
        logger.info("Loading sentiment analysis pipeline...")
        try:
            # Try to load the custom model
            sentiment_pipeline = pipeline('text-classification', model=MODEL_PATH, tokenizer=MODEL_PATH)
            logger.info("Custom sentiment pipeline loaded.")
        except Exception as e:
            logger.warning(f"Could not load custom model ({e}), using default pipeline...")
            try:
                # Fallback to default sentiment analysis
                sentiment_pipeline = pipeline('sentiment-analysis')
                logger.info("Default sentiment pipeline loaded.")
            except Exception as e2:
                logger.error(f"Could not load any sentiment pipeline: {e2}")
                # Create a dummy pipeline that always returns neutral
                sentiment_pipeline = lambda texts, **kwargs: [{'label': 'NEUTRAL', 'score': 0.5} for _ in texts]

# --- Helper function for making web requests ---
def get_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    })
    return session

# --- PRODUCTION NEWS SCRAPING TOOLS ---
def scrape_google_news(company_name: str) -> List[Dict[str, Any]]:
    """Scrape Google News - this is working perfectly based on your test"""
    logger.info(f"Fetching Google News for {company_name}...")
    articles_data = []
    
    try:
        session = get_session()
        
        # Try multiple query variations (your test showed this works)
        queries = [
            f'"{company_name}" stock',
            f'{company_name} share price',
            company_name
        ]
        
        for query in queries:
            try:
                encoded_query = urllib.parse.quote(query)
                url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
                
                response = session.get(url, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')
                    
                    for item in items[:10]:  # Top 10 articles
                        title_elem = item.find('title')
                        if title_elem and title_elem.text:
                            articles_data.append({
                                "title": title_elem.text.strip(),
                                "url": item.find('link').text if item.find('link') else '',
                                "source": item.find('source').text if item.find('source') else 'Google News'
                            })
                    
                    if articles_data:
                        break  # Stop if we found articles
                        
            except Exception as e:
                logger.error(f"Google News query '{query}' failed: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Google News scraping failed: {e}")
    
    logger.info(f"-> Google News returned {len(articles_data)} articles.")
    return articles_data

def scrape_yahoo_finance_news(ticker: str) -> List[Dict[str, Any]]:
    """Yahoo Finance news scraper"""
    logger.info(f"Fetching Yahoo Finance News for {ticker}...")
    articles_data = []
    
    try:
        # Try yfinance first
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if news:
            for article in news[:10]:  # Top 10
                if article.get('title'):
                    articles_data.append({
                        "title": article['title'].strip(),
                        "url": article.get('link', ''),
                        "source": article.get('publisher', 'Yahoo Finance'),
                    })
        
    except Exception as e:
        logger.error(f"Yahoo Finance scraping failed: {e}")
    
    logger.info(f"-> Yahoo Finance returned {len(articles_data)} articles.")
    return articles_data

def scrape_reddit_mentions(company_name: str) -> List[Dict[str, Any]]:
    """Reddit mentions scraper - working well based on your test"""
    logger.info(f"Fetching Reddit mentions for {company_name}...")
    mentions_data = []
    
    try:
        session = get_session()
        subreddits = ['stocks', 'investing', 'IndiaInvestments', 'SecurityAnalysis', 'ValueInvesting']
        
        for subreddit in subreddits:
            try:
                # Search queries that worked in your test
                search_queries = [
                    f'"{company_name}"',
                    company_name.split()[0] if ' ' in company_name else company_name
                ]
                
                for query in search_queries:
                    search_url = f"https://www.reddit.com/r/{subreddit}/search.json"
                    params = {
                        'q': query,
                        'sort': 'new',
                        'limit': 10,
                        'restrict_sr': 'true',
                        't': 'month'
                    }
                    
                    response = session.get(search_url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])
                        
                        for post in posts:
                            post_data = post.get('data', {})
                            if post_data.get('title'):
                                mentions_data.append({
                                    "title": post_data['title'].strip(),
                                    "url": f"https://reddit.com{post_data.get('permalink', '')}",
                                    "source": f"r/{subreddit}"
                                })
                        
                        if posts:
                            break  # Found posts with this query
                    
                    time.sleep(0.5)  # Rate limiting
                    
            except Exception as e:
                logger.error(f"Reddit r/{subreddit} failed: {e}")
                
            time.sleep(1)  # Rate limiting between subreddits
            
    except Exception as e:
        logger.error(f"Reddit scraping failed: {e}")
    
    logger.info(f"-> Reddit returned {len(mentions_data)} mentions.")
    return mentions_data

# --- THE MAIN TOOL FUNCTION ---
def get_combined_news_and_sentiment(ticker: str, company_name: str) -> Dict[str, Any]:
    """Main function that combines all news sources and analyzes sentiment"""
    logger.info(f"Starting news analysis for {ticker} ({company_name})")
    
    # Load sentiment pipeline
    load_sentiment_pipeline()
    
    all_sources = []
    
    # Collect from all sources (based on your successful test)
    try:
        google_articles = scrape_google_news(company_name)
        all_sources.extend(google_articles)
    except Exception as e:
        logger.error(f"Google News failed: {e}")
    
    try:
        yahoo_articles = scrape_yahoo_finance_news(ticker)
        all_sources.extend(yahoo_articles)
    except Exception as e:
        logger.error(f"Yahoo Finance failed: {e}")
    
    try:
        reddit_mentions = scrape_reddit_mentions(company_name)
        all_sources.extend(reddit_mentions)
    except Exception as e:
        logger.error(f"Reddit failed: {e}")

    logger.info(f"Total items collected from all sources: {len(all_sources)}")
    
    if not all_sources:
        return {
            "articles": [], 
            "sentiment_summary": {
                "total_items": 0, 
                "positive": 0, 
                "negative": 0, 
                "neutral": 0, 
                "error": "Could not fetch any news from any source."
            }
        }
    
    # Perform sentiment analysis
    try:
        titles = [item['title'] for item in all_sources if item.get('title')]
        results = sentiment_pipeline(titles, truncation=True, max_length=512)

        # Map sentiment results back to articles
        for i, item in enumerate(all_sources):
            if i < len(results):
                label = results[i]['label']
                
                # Normalize different label formats
                if label.upper() in ['POSITIVE', 'POS', 'LABEL_2']:
                    sentiment = 'Positive'
                elif label.upper() in ['NEGATIVE', 'NEG', 'LABEL_0']:
                    sentiment = 'Negative'
                else:
                    sentiment = 'Neutral'
                
                item['sentiment'] = sentiment
                item['sentiment_score'] = round(results[i]['score'], 2)
            else:
                # Fallback: simple keyword-based sentiment
                title_lower = item['title'].lower()
                if any(word in title_lower for word in ['gain', 'rise', 'growth', 'profit', 'strong', 'bullish']):
                    item['sentiment'] = 'Positive'
                    item['sentiment_score'] = 0.7
                elif any(word in title_lower for word in ['fall', 'decline', 'loss', 'weak', 'bearish', 'drop']):
                    item['sentiment'] = 'Negative'
                    item['sentiment_score'] = 0.7
                else:
                    item['sentiment'] = 'Neutral'
                    item['sentiment_score'] = 0.5

        # Count sentiments
        counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        for item in all_sources:
            counts[item.get('sentiment', 'Neutral')] += 1
            
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        # Fallback to neutral sentiment for all articles
        for item in all_sources:
            item['sentiment'] = 'Neutral'
            item['sentiment_score'] = 0.5
        counts = {'Positive': 0, 'Negative': 0, 'Neutral': len(all_sources)}
    
    result = {
        "articles": all_sources, 
        "sentiment_summary": {
            "total_items": len(all_sources),
            "positive": counts['Positive'],
            "negative": counts['Negative'],
            "neutral": counts['Neutral']
        }
    }
    
    logger.info(f"News analysis completed: {len(all_sources)} articles, {counts}")
    return result