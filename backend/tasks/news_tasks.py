# # tasks/news_tasks.py - SIMPLIFIED VERSION THAT ALWAYS WORKS

# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from uuid import UUID
# import logging
# from datetime import datetime
# import yfinance as yf

# logger = logging.getLogger(__name__)

# def get_stock_basic_info(ticker: str):
#     """Get basic stock information to create realistic content"""
#     try:
#         stock = yf.Ticker(ticker)
#         info = stock.info
#         return {
#             'name': info.get('longName', ticker.replace('.NS', '')),
#             'sector': info.get('sector', 'Unknown'),
#             'industry': info.get('industry', 'Unknown'),
#             'current_price': info.get('currentPrice', 0),
#             'previous_close': info.get('previousClose', 0)
#         }
#     except Exception as e:
#         logger.warning(f"Could not get stock info for {ticker}: {e}")
#         return {
#             'name': ticker.replace('.NS', ''),
#             'sector': 'Unknown',
#             'industry': 'Unknown', 
#             'current_price': 0,
#             'previous_close': 0
#         }

# def create_realistic_articles(ticker: str, company_name: str, stock_info: dict):
#     """Create realistic articles based on stock information"""
    
#     # Calculate price movement for realistic sentiment
#     current_price = stock_info.get('current_price', 0)
#     previous_close = stock_info.get('previous_close', 0) 
    
#     price_change = 0
#     if current_price and previous_close:
#         price_change = ((current_price - previous_close) / previous_close) * 100
    
#     # Generate articles based on actual stock performance
#     articles = []
    
#     if price_change > 2:
#         articles.extend([
#             {
#                 "title": f"{company_name} Shares Rally {price_change:.1f}% on Strong Market Sentiment",
#                 "url": f"https://finance.yahoo.com/quote/{ticker}",
#                 "source": "Market Analysis",
#                 "sentiment": "Positive",
#                 "sentiment_score": 0.8
#             },
#             {
#                 "title": f"Investors Show Confidence in {company_name} as Stock Gains Momentum",
#                 "url": f"https://www.moneycontrol.com/india/stockpricequote/{ticker}",
#                 "source": "Financial Express",
#                 "sentiment": "Positive",
#                 "sentiment_score": 0.7
#             }
#         ])
#     elif price_change < -2:
#         articles.extend([
#             {
#                 "title": f"{company_name} Stock Declines {abs(price_change):.1f}% Amid Market Volatility",
#                 "url": f"https://finance.yahoo.com/quote/{ticker}",
#                 "source": "Market Watch",
#                 "sentiment": "Negative",
#                 "sentiment_score": 0.8
#             },
#             {
#                 "title": f"Market Correction Impacts {company_name} Share Price",
#                 "url": f"https://www.moneycontrol.com/india/stockpricequote/{ticker}",
#                 "source": "Economic Times",
#                 "sentiment": "Negative", 
#                 "sentiment_score": 0.6
#             }
#         ])
#     else:
#         articles.extend([
#             {
#                 "title": f"{company_name} Stock Shows Steady Performance in Current Market",
#                 "url": f"https://finance.yahoo.com/quote/{ticker}",
#                 "source": "Yahoo Finance",
#                 "sentiment": "Neutral",
#                 "sentiment_score": 0.5
#             },
#             {
#                 "title": f"Technical Analysis: {company_name} Maintains Stable Trading Range", 
#                 "url": f"https://www.moneycontrol.com/india/stockpricequote/{ticker}",
#                 "source": "Market Analysis",
#                 "sentiment": "Neutral",
#                 "sentiment_score": 0.5
#             }
#         ])
    
#     # Add sector-specific articles
#     sector = stock_info.get('sector', 'Unknown')
#     if sector != 'Unknown':
#         articles.extend([
#             {
#                 "title": f"{sector} Sector Update: Key Players Including {company_name} in Focus",
#                 "url": "https://example.com/sector-analysis",
#                 "source": "Sector Reports",
#                 "sentiment": "Neutral",
#                 "sentiment_score": 0.6
#             },
#             {
#                 "title": f"Industry Outlook: {stock_info.get('industry', 'Market')} Trends Affecting {company_name}",
#                 "url": "https://example.com/industry-outlook", 
#                 "source": "Industry Analysis",
#                 "sentiment": "Positive",
#                 "sentiment_score": 0.6
#             }
#         ])
    
#     # Add general market articles
#     articles.extend([
#         {
#             "title": f"Quarterly Performance Review: {company_name} Financials and Market Position",
#             "url": f"https://finance.yahoo.com/quote/{ticker}/financials",
#             "source": "Financial Reports",
#             "sentiment": "Neutral",
#             "sentiment_score": 0.5
#         },
#         {
#             "title": f"Analyst Coverage: Investment Recommendations for {company_name} Stock",
#             "url": "https://example.com/analyst-coverage",
#             "source": "Research Reports", 
#             "sentiment": "Positive",
#             "sentiment_score": 0.7
#         },
#         {
#             "title": f"Market Sentiment Analysis: Retail vs Institutional Interest in {company_name}",
#             "url": "https://example.com/market-sentiment",
#             "source": "Market Research",
#             "sentiment": "Neutral",
#             "sentiment_score": 0.5
#         }
#     ])
    
#     return articles[:8]  # Return top 8 articles

# def try_real_news_sources(ticker: str, company_name: str):
#     """Attempt to get real news, but don't fail if it doesn't work"""
#     real_articles = []
    
#     try:
#         # Try Yahoo Finance news (most reliable)
#         logger.info(f"Attempting to fetch real Yahoo Finance news for {ticker}")
#         stock = yf.Ticker(ticker)
#         news = stock.news
        
#         if news:
#             logger.info(f"Found {len(news)} Yahoo Finance articles")
#             for article in news[:5]:  # Take first 5
#                 if article.get('title'):
#                     # Simple sentiment analysis
#                     title_lower = article['title'].lower()
#                     if any(word in title_lower for word in ['gain', 'rise', 'growth', 'profit', 'strong']):
#                         sentiment = 'Positive'
#                         score = 0.7
#                     elif any(word in title_lower for word in ['fall', 'decline', 'loss', 'weak', 'drop']):
#                         sentiment = 'Negative'
#                         score = 0.7
#                     else:
#                         sentiment = 'Neutral'
#                         score = 0.5
                    
#                     real_articles.append({
#                         "title": article['title'].strip(),
#                         "url": article.get('link', ''),
#                         "source": article.get('publisher', 'Yahoo Finance'),
#                         "sentiment": sentiment,
#                         "sentiment_score": score,
#                         "is_real": True
#                     })
        
#         logger.info(f"Successfully retrieved {len(real_articles)} real articles")
        
#     except Exception as e:
#         logger.warning(f"Could not fetch real news: {e}")
    
#     return real_articles

# @celery.task
# def run_intelligence_analysis(job_id: str):
#     """Simplified intelligence analysis that always provides results"""
#     db = SessionLocal()
#     job = None
    
#     try:
#         logger.info(f"Starting intelligence analysis for job {job_id}")
        
#         # Get job
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job or not job.result:
#             raise ValueError(f"Job {job_id} not found or has no initial data.")
        
#         job.status = "INTELLIGENCE_GATHERING"
#         db.commit()
        
#         current_data = job.result
#         ticker = current_data.get("ticker")
#         company_name = current_data.get("company_name", ticker.replace('.NS', ''))
        
#         logger.info(f"Analyzing {company_name} ({ticker})")
        
#         # Get basic stock information
#         stock_info = get_stock_basic_info(ticker)
#         logger.info(f"Stock info: {stock_info['name']} - {stock_info['sector']}")
        
#         # Try to get real news first
#         real_articles = try_real_news_sources(ticker, company_name)
        
#         # Create realistic articles
#         realistic_articles = create_realistic_articles(ticker, company_name, stock_info)
        
#         # Combine real and realistic articles
#         all_articles = real_articles + realistic_articles
        
#         # Remove duplicates and limit to 10 articles
#         seen_titles = set()
#         unique_articles = []
#         for article in all_articles:
#             if article['title'] not in seen_titles:
#                 seen_titles.add(article['title'])
#                 unique_articles.append(article)
        
#         final_articles = unique_articles[:10]
        
#         # Count sentiments
#         sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
#         for article in final_articles:
#             sentiment_counts[article['sentiment']] += 1
        
#         # Create intelligence briefing
#         intelligence_briefing = {
#             "articles": final_articles,
#             "sentiment_summary": {
#                 "total_items": len(final_articles),
#                 "positive": sentiment_counts['Positive'],
#                 "negative": sentiment_counts['Negative'],
#                 "neutral": sentiment_counts['Neutral'],
#                 "real_articles": len(real_articles),
#                 "generated_articles": len(realistic_articles),
#                 "analysis_timestamp": datetime.now().isoformat()
#             }
#         }
        
#         # Update job result
#         new_result = current_data.copy()
#         new_result['intelligence_briefing'] = intelligence_briefing
#         job.result = new_result
#         job.status = "INTELLIGENCE_COMPLETE"
        
#         db.commit()
        
#         logger.info(f"Intelligence analysis completed successfully:")
#         logger.info(f"- Total articles: {len(final_articles)}")
#         logger.info(f"- Real articles: {len(real_articles)}")
#         logger.info(f"- Generated articles: {len(realistic_articles)}")
#         logger.info(f"- Sentiment: {sentiment_counts}")
        
#         return str(job.result)
        
#     except Exception as e:
#         logger.error(f"Intelligence analysis failed for job {job_id}: {e}")
        
#         if job:
#             job.status = "FAILED"
#             error_data = job.result if job.result else {}
#             error_data['error'] = f"Intelligence analysis failed: {str(e)}"
#             job.result = error_data
#             db.commit()
        
#         return f"Error: {e}"
        
#     finally:
#         db.close()









# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.news_tools import get_combined_news_and_sentiment
# from uuid import UUID

# @celery.task
# def run_intelligence_analysis(job_id: str):
#     with SessionLocal() as db:
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job or not job.result:
#             print(f"Job {job_id} not found or has no data for intelligence.")
#             return
        
#         try:
#             job.status = "INTELLIGENCE_GATHERING"
#             db.commit()

#             current_data = job.result
#             ticker = current_data.get("ticker")
#             company_name = current_data.get("company_name")
            
#             intelligence_briefing = get_combined_news_and_sentiment(ticker, company_name)
            
#             new_result = dict(current_data)
#             new_result['intelligence_briefing'] = intelligence_briefing
#             job.result = new_result
            
#             db.commit()
#             print(f"Intelligence analysis for job {job_id} completed successfully.")
#             return "Intelligence gathering successful."
#         except Exception as e:
#             print(f"Error during intelligence analysis for job {job_id}: {e}")
#             job.status = "FAILED"
#             error_data = job.result if job.result else {}
#             error_data['error'] = f"Intelligence analysis failed: {str(e)}"
#             job.result = error_data
#             db.commit()
#             return f"Intelligence gathering failed: {e}"








from celery_worker import celery
from tools.news_tools import get_combined_news_and_sentiment

@celery.task
def get_intelligence_task(ticker: str, company_name: str):
    print(f"Executing get_intelligence_task for {company_name}...")
    # This task now depends on the company_name from the first task's result
    return get_combined_news_and_sentiment(ticker, company_name)