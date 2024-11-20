import json

def pretty_hotel_output(data: list):
    if not data:
        return None
    try:
        return json.dumps(data.model_dump(mode = "json"), indent = 4)
    except Exception as e:
        raise Exception(f'Error when converting hotel to json: {e}')
    
def pretty_hotels_output(data):
    if not data:
        return []
    try:
        result = []
        for hotel in data.hotels:
            result.append(hotel)
        return result
    except Exception as e:
        raise Exception(f'Error when converting hotels to json: {e}')
