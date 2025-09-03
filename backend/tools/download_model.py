from sentence_transformers import CrossEncoder
import os

# Define the model name and the directory to save it to
MODEL_NAME = 'cross-encoder/nli-roberta-base'
MODEL_PATH = './sentiment_model'

def main():
    """
    Downloads the specified model from Hugging Face and saves it locally.
    """
    print(f"Downloading model: {MODEL_NAME}")
    
    # Check if the directory exists
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
        
    # This command downloads the model and saves it to the specified path
    model = CrossEncoder(MODEL_NAME)
    model.save(MODEL_PATH)
    
    print(f"Model downloaded and saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()