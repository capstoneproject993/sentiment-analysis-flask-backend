import pickle

with open('model_deeplearning (1).pkl', 'rb') as file:
    loaded_model = pickle.load(file)

print("Model loaded successfully!")
