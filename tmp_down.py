from transformers import pipeline

print("Downloading NEW model 'ProsusAI/finbert'...")
classifier = pipeline('text-classification', model='ProsusAI/finbert')
print("Download complete!")