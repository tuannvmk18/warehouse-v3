def update_model(obj, data):
    for key, value in data.items():
        setattr(obj, key, value)
