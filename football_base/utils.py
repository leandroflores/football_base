
def update_attributes(object: object, data: dict) -> object:
    for key, value in data.items():
        if hasattr(object, key):
            setattr(object, key, value)