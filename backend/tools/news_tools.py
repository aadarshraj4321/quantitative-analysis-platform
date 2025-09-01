import snscrape.modules.twitter as sntwitter
import newspaper
# We will now import AutoModelForSequenceClassification and AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch # We need torch to process the model's output
from typing import List, Dict, Any

# We will load the model and tokenizer inside the function
sentiment_model = None
tokenizer = None
MODEL_PATH = '/code/sentiment_model'

def load_sentiment_model():
    """A function to load the model and tokenizer on demand using the transformers library."""
    global sentiment_model, tokenizer
    if sentiment_model is None or tokenizer is None:
        print("Loading sentiment model and tokenizer for the first time...")
        # Load the tokenizer from the local path
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        # Load the model from the local path
        sentiment_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        print("Sentiment model and tokenizer loaded.")

def analyze_sentiment_with_model(text: str) -> str:
    """Uses the loaded model to predict sentiment."""
    # This is the standard way to use a transformers model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = sentiment_model(**inputs).logits
    
    scores = logits.softmax(dim=1)[0].tolist()
    sentiment_map = {0: 'Positive', 1: 'Neutral', 2: 'Negative'} # This order might be different
    
    # Let's verify the model's expected labels
    model_labels = sentiment_model.config.id2label
    if model_labels:
        # e.g., {0: 'positive', 1: 'neutral', 2: 'negative'}
        sentiment_map = {int(k): v.capitalize() for k, v in model_labels.items()}

    best_index = scores.index(max(scores))
    return sentiment_map.get(best_index, "Unknown")


def get_news_and_sentiment(ticker: str, company_name: str) -> List[Dict[str, Any]]:
    load_sentiment_model()
    
    print(f"Fetching news for {company_name}...")
    search_url = f"https://news.google.com/rss/search?q={company_name.replace(' ', '+')}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    news_source = newspaper.build(search_url, memoize_articles=False, language='en')
    articles_data = []
    for article in news_source.articles[:5]:
        try:
            article.download(); article.parse(); article.nlp()
            if not article.text or len(article.text) < 150: continue

            sentiment = analyze_sentiment_with_model(article.summary)

            articles_data.append({
                "title": article.title,
                "summary": article.summary,
                "url": article.url,
                "sentiment": sentiment
            })
        except Exception as e:
            print(f"Could not process article {article.url}: {e}")
    return articles_data

def get_twitter_sentiment(search_query: str) -> Dict[str, Any]:
    load_sentiment_model()

    print(f"Fetching Twitter sentiment for '{search_query}'...")
    tweets = [tweet.rawContent for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{search_query} lang:en").get_items()) if i < 50]
    if not tweets: return {"error": "No recent tweets found."}

    counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0, 'Unknown': 0}
    for text in tweets:
        sentiment = analyze_sentiment_with_model(text)
        counts[sentiment] += 1
    
    return {
        "search_query": search_query,
        "total_tweets": len(tweets),
        "positive": counts['Positive'],
        "negative": counts['Negative'],
        "neutral": counts['Neutral']
    }