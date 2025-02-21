import pickle
from app.core.config import settings

def load_model():
    with open(settings.MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()
