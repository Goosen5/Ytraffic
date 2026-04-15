import pickle


def save_model(model, path: str) -> None:
    # persist model for later reuse
    with open(path, "wb") as file_obj:
        pickle.dump(model, file_obj)
    print(f"Model saved to {path}")


def load_model(path: str):
    # load already trained model from disk
    with open(path, "rb") as file_obj:
        return pickle.load(file_obj)
