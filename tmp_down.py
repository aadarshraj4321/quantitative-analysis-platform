from sentence_transformers import CrossEncoder

print("Starting model download to local cache...")
# This will download the model to a central Hugging Face cache on your Mac
# It might be in ~/.cache/huggingface/hub/ or similar
model = CrossEncoder('cross-encoder/nli-roberta-base')
print("Model download complete!")