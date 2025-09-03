from transformers import pipeline

print("Downloading NEW model 'ProsusAI/finbert'...")
# Using the pipeline API is the easiest way to download all necessary files
classifier = pipeline('text-classification', model='ProsusAI/finbert')
print("Download complete!")