import pickle


def save_data(data, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_data(filename: str):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
