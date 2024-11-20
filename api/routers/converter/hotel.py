import json

def convert(data):
    if not data:
        return None
    try:
        return json.dumps([data.model_dump(mode = "json")], indent = 4)
    except Exception as e:
        raise Exception(f'Error when converting hotel to json: {e}')