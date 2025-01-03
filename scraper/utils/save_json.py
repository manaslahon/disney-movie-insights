import pickle
import json


def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii= False, indent= 2)
 
 
def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)

def save_data_pickle(name, data):
    with open(name, 'wb') as f:
        pickle.dump(data, f)

def load_data_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)
