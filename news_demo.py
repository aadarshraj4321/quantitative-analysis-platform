import requests
import yfinance as yf
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta
import json
import re
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import urllib.parse

class FreeStockSentimentAnalyzer:
    def __init__(self):
        """
        Initialize the Free Stock Sentiment Analyzer
        Uses only free APIs and web scraping methods
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get basic stock information using yfinance (free)
        """
        try:
            # Try different suffix combinations for Indian stocks
            suffixes_to_try = [
                symbol.upper(),  # As is (for US stocks)
                f"{symbol.upper()}.NS",  # NSE
                f"{symbol.upper()}.BO",  # BSE
            ]
            
            stock_info = None
            working_symbol = None
            
            for test_symbol in suffixes_to_try:
                try:
                    stock = yf.Ticker(test_symbol)
                    info = stock.info
                    hist = stock.history(period="1d")
                    
                    # Check if we got valid data
                    if not hist.empty or 'symbol' in info or 'shortName' in info:
                        stock_info = info
                        working_symbol = test_symbol
                        
                        # Get current price from history if not in info
                        if not hist.empty:
                            current_price = hist['Close'].iloc[-1]
                        else:
                            current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                        
                        break
                except Exception as e:
                    continue
            
            if stock_info:
                return {
                    'symbol': working_symbol,
                    'name': stock_info.get('longName', stock_info.get('shortName', symbol)),
                    'sector': stock_info.get('sector', 'N/A'),
                    'country': stock_info.get('country', 'N/A'),
                    'currency': stock_info.get('currency', 'N/A'),
                    'market_cap': stock_info.get('marketCap', 'N/A'),
                    'current_price': current_price
                }
            else:
                return {
                    'symbol': symbol,
                    'name': symbol,
                    'sector': 'N/A',
                    'country': 'N/A',
                    'currency': 'N/A',
                    'market_cap': 'N/A',
                    'current_price': 'N/A'
                }
                
        except Exception as e:
            print(f"Error getting stock info: {e}")
            return {
                'symbol': symbol,
                'name': symbol,
                'sector': 'N/A',
                'country': 'N/A',
                'currency': 'N/A',
                'market_cap': 'N/A',
                'current_price': 'N/A'
            }
    
    def scrape_google_news(self, stock_name: str, company_name: str) -> List[Dict]:
        """
        Scrape news from Google News (free method)
        """
        try:
            # Create search query for Google News
            query = f"{company_name} stock news"
            encoded_query = urllib.parse.quote(query)
            
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                articles = []
                for item in items[:15]:  # Limit to 15 articles
                    try:
                        title = item.find('title').text if item.find('title') else ''
                        link = item.find('link').text if item.find('link') else ''
                        pub_date = item.find('pubDate').text if item.find('pubDate') else ''
                        description = item.find('description').text if item.find('description') else ''
                        source = item.find('source').text if item.find('source') else 'Google News'
                        
                        articles.append({
                            'title': title,
                            'description': BeautifulSoup(description, 'html.parser').get_text()[:200] if description else '',
                            'url': link,
                            'published_at': pub_date,
                            'source': source,
                        })
                    except Exception as e:
                        continue
                
                return articles
            else:
                print(f"Google News scraping failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error scraping Google News: {e}")
            return []
    
    def scrape_yahoo_news(self, symbol: str) -> List[Dict]:
        """
        Scrape news from Yahoo Finance (free method)
        """
        try:
            # Try different symbol formats
            symbols_to_try = [symbol, f"{symbol}.NS", f"{symbol}.BO"]
            
            articles = []
            for test_symbol in symbols_to_try:
                try:
                    stock = yf.Ticker(test_symbol)
                    news = stock.news
                    
                    for article in news[:10]:  # Limit to 10 articles per symbol
                        articles.append({
                            'title': article.get('title', ''),
                            'description': article.get('summary', ''),
                            'url': article.get('link', ''),
                            'published_at': datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S') if article.get('providerPublishTime') else '',
                            'source': article.get('publisher', 'Yahoo Finance'),
                        })
                    
                    if articles:  # If we found articles, stop trying other symbols
                        break
                        
                except Exception as e:
                    continue
            
            return articles
            
        except Exception as e:
            print(f"Error scraping Yahoo News: {e}")
            return []
    
    def scrape_reddit_mentions(self, stock_name: str, company_name: str) -> List[Dict]:
        """
        Scrape Reddit mentions using Reddit's JSON API (free)
        """
        try:
            # Search multiple subreddits
            subreddits = ['stocks', 'investing', 'SecurityAnalysis', 'StockMarket', 'ValueInvesting']
            mentions = []
            
            for subreddit in subreddits:
                try:
                    # Search for posts mentioning the stock
                    search_url = f"https://www.reddit.com/r/{subreddit}/search.json"
                    params = {
                        'q': f"{stock_name} OR {company_name}",
                        'sort': 'new',
                        'limit': 10,
                        'restrict_sr': 'true'
                    }
                    
                    response = self.session.get(search_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])
                        
                        for post in posts:
                            post_data = post.get('data', {})
                            mentions.append({
                                'title': post_data.get('title', ''),
                                'text': post_data.get('selftext', ''),
                                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                'score': post_data.get('score', 0),
                                'created_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                                'subreddit': subreddit,
                                'author': post_data.get('author', 'Unknown'),
                                'num_comments': post_data.get('num_comments', 0)
                            })
                    
                    time.sleep(1)  # Be respectful to Reddit's servers
                    
                except Exception as e:
                    print(f"Error scraping r/{subreddit}: {e}")
                    continue
            
            return mentions[:20]  # Return top 20 mentions
            
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            return []
    
    def get_free_twitter_alternative(self, stock_name: str, company_name: str) -> List[Dict]:
        """
        Get social media mentions from free sources (alternative to Twitter API)
        This is a placeholder for free social media data sources
        """
        try:
            # Using Reddit as Twitter alternative since Twitter API is no longer free
            print("Note: Using Reddit data as Twitter alternative (Twitter API no longer free)")
            return self.scrape_reddit_mentions(stock_name, company_name)
            
        except Exception as e:
            print(f"Error getting social media data: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob (free library)
        """
        try:
            if not text or text.strip() == '':
                return {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment_label': 'Neutral'}
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
            
            # Determine sentiment label
            if polarity > 0.1:
                sentiment_label = 'Positive'
            elif polarity < -0.1:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment_label': sentiment_label
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment_label': 'Neutral'}
    
    def calculate_overall_sentiment(self, articles: List[Dict]) -> Dict:
        """
        Calculate overall sentiment from all articles/posts
        """
        if not articles:
            return {
                'overall_sentiment': 'Neutral',
                'average_polarity': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_articles': 0
            }
        
        polarities = []
        sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        
        for article in articles:
            if 'sentiment' in article:
                polarity = article['sentiment']['polarity']
                sentiment_label = article['sentiment']['sentiment_label']
                
                polarities.append(polarity)
                sentiment_counts[sentiment_label] += 1
        
        if polarities:
            avg_polarity = sum(polarities) / len(polarities)
            
            if avg_polarity > 0.05:
                overall_sentiment = 'Positive'
            elif avg_polarity < -0.05:
                overall_sentiment = 'Negative'
            else:
                overall_sentiment = 'Neutral'
        else:
            avg_polarity = 0.0
            overall_sentiment = 'Neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'average_polarity': round(avg_polarity, 3),
            'positive_count': sentiment_counts['Positive'],
            'negative_count': sentiment_counts['Negative'],
            'neutral_count': sentiment_counts['Neutral'],
            'total_articles': len(articles)
        }
    
    def analyze_stock(self, symbol: str) -> Dict:
        """
        Main function to analyze a stock comprehensively
        """
        print(f"Analyzing stock: {symbol}")
        print("=" * 50)
        
        # Get stock information
        print("Fetching stock information...")
        stock_info = self.get_stock_info(symbol)
        
        company_name = stock_info['name']
        stock_symbol = stock_info['symbol']
        
        print(f"Company: {company_name}")
        print(f"Symbol: {stock_symbol}")
        
        # Collect all news and social media data
        all_articles = []
        
        # Get news from different sources
        print("\nFetching news from Google News...")
        google_news = self.scrape_google_news(symbol, company_name)
        all_articles.extend(google_news)
        
        print("Fetching news from Yahoo Finance...")
        yahoo_news = self.scrape_yahoo_news(symbol)
        all_articles.extend(yahoo_news)
        
        print("Fetching social media mentions...")
        social_mentions = self.get_free_twitter_alternative(symbol, company_name)
        all_articles.extend(social_mentions)
        
        # Analyze sentiment for each article
        print(f"\nAnalyzing sentiment for {len(all_articles)} items...")
        for article in all_articles:
            text_to_analyze = ""
            
            # Combine title and description/text for sentiment analysis
            if 'title' in article and article['title']:
                text_to_analyze += article['title'] + " "
            
            if 'description' in article and article['description']:
                text_to_analyze += article['description']
            elif 'text' in article and article['text']:
                text_to_analyze += article['text']
            
            article['sentiment'] = self.analyze_sentiment(text_to_analyze)
        
        # Calculate overall sentiment
        overall_sentiment = self.calculate_overall_sentiment(all_articles)
        
        # Compile results
        results = {
            'stock_info': stock_info,
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_items_analyzed': len(all_articles),
            'news_articles': [article for article in all_articles if 'subreddit' not in article],
            'social_media_mentions': [article for article in all_articles if 'subreddit' in article],
            'sentiment_analysis': overall_sentiment,
            'articles_with_sentiment': all_articles
        }
        
        return results
    
    def print_results(self, results: Dict):
        """
        Print formatted results
        """
        print("\n" + "="*80)
        print("STOCK SENTIMENT ANALYSIS REPORT")
        print("="*80)
        
        # Stock Information
        stock_info = results['stock_info']
        print(f"\n📊 STOCK INFORMATION:")
        print(f"   Symbol: {stock_info['symbol']}")
        print(f"   Company: {stock_info['name']}")
        print(f"   Sector: {stock_info['sector']}")
        print(f"   Country: {stock_info['country']}")
        print(f"   Current Price: {stock_info['current_price']} {stock_info['currency']}")
        print(f"   Market Cap: {stock_info['market_cap']}")
        
        # Sentiment Summary
        sentiment = results['sentiment_analysis']
        print(f"\n🎯 SENTIMENT ANALYSIS SUMMARY:")
        print(f"   Overall Sentiment: {sentiment['overall_sentiment']}")
        print(f"   Average Polarity: {sentiment['average_polarity']}")
        print(f"   Positive Articles: {sentiment['positive_count']}")
        print(f"   Negative Articles: {sentiment['negative_count']}")
        print(f"   Neutral Articles: {sentiment['neutral_count']}")
        print(f"   Total Items Analyzed: {sentiment['total_articles']}")
        
        # Recent News
        news_articles = results['news_articles']
        if news_articles:
            print(f"\n📰 LATEST NEWS ({len(news_articles)} articles):")
            for i, article in enumerate(news_articles[:5], 1):
                sentiment_info = article.get('sentiment', {})
                print(f"\n   {i}. {article['title'][:80]}...")
                print(f"      Source: {article['source']}")
                print(f"      Sentiment: {sentiment_info.get('sentiment_label', 'N/A')} "
                      f"(Polarity: {sentiment_info.get('polarity', 'N/A')})")
                print(f"      URL: {article['url']}")
        
        # Social Media Mentions
        social_mentions = results['social_media_mentions']
        if social_mentions:
            print(f"\n💬 SOCIAL MEDIA MENTIONS ({len(social_mentions)} mentions):")
            for i, mention in enumerate(social_mentions[:5], 1):
                sentiment_info = mention.get('sentiment', {})
                print(f"\n   {i}. r/{mention.get('subreddit', 'unknown')}: {mention['title'][:60]}...")
                print(f"      Score: {mention.get('score', 0)} | Comments: {mention.get('num_comments', 0)}")
                print(f"      Sentiment: {sentiment_info.get('sentiment_label', 'N/A')} "
                      f"(Polarity: {sentiment_info.get('polarity', 'N/A')})")
        
        print(f"\n⏰ Analysis completed at: {results['analysis_timestamp']}")
        print("="*80)

# Example usage and main function
def main():
    """
    Main function to run the stock sentiment analyzer
    """
    analyzer = FreeStockSentimentAnalyzer()
    
    while True:
        print("\n🔍 Free Stock Sentiment Analyzer")
        print("-" * 40)
        stock_symbol = input("Enter stock symbol (e.g., RELIANCE, AAPL, TCS): ").strip()
        
        if not stock_symbol:
            print("Please enter a valid stock symbol.")
            continue
        
        if stock_symbol.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        try:
            # Analyze the stock
            results = analyzer.analyze_stock(stock_symbol)
            
            # Print results
            analyzer.print_results(results)
            
            # Ask if user wants to save results
            save_option = input("\nWould you like to save results to JSON file? (y/n): ").strip().lower()
            if save_option == 'y':
                filename = f"{stock_symbol}_sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"Results saved to {filename}")
            
        except Exception as e:
            print(f"Error analyzing stock {stock_symbol}: {e}")
        
        # Ask if user wants to analyze another stock
        continue_option = input("\nAnalyze another stock? (y/n): ").strip().lower()
        if continue_option != 'y':
            print("Thank you for using Stock Sentiment Analyzer!")
            break

if __name__ == "__main__":
    print("Welcome to Free Stock Sentiment Analyzer!")
    print("\nRequired Python packages:")
    print("pip install yfinance textblob pandas beautifulsoup4 requests lxml")
    print("\nNote: This tool uses free APIs and web scraping methods only.")
    print("For Twitter data, we use Reddit as an alternative since Twitter API is no longer free.")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")