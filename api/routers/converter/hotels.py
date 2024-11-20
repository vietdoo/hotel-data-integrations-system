import json

def convert(data):
    if not data:
        return None
    try:
        return json.dumps([hotel.model_dump(mode = "json") for hotel in data.hotels], 
                          indent=4)
    except Exception as e:
        raise Exception(f'Error when converting hotel to json: {e}')
