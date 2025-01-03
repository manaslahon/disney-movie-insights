import pickle
import json
import os

def save_data(title, data, directory='dataset'):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, title)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii= False, indent= 2)
 
 
def load_data(title, directory='dataset'):
    file_path = os.path.join(directory, title)
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

def save_data_pickle(title, data, directory='dataset'):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, title)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_data_pickle(title, directory='dataset'):
    file_path = os.path.join(directory, title)
    with open(file_path, 'rb') as f:
        return pickle.load(f)
