from sentence_transformers import SentenceTransformer

# Load pretrained transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_model():
    return model