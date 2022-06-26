import json

def construct_path(*args, entry_point = "flask-response") -> str:
    
    """Constructs path using the passed chain of arguments"""
    
    args = [arg.lower() for arg in args]
    extension = "/".join(args)
    path = f"{entry_point}/{extension}"
    return path

def load_json(filename) -> dict:
    
    """Fetches JSON data (returned as a python dictionary) from the passed filename"""

    try:
        
        with open(filename, 'r') as file:
            json_data = json.load(file)
        return json_data
    
    except:
        
        return { }
    
def post_json(filename, json_data) -> None:
    
    """Posts dictionary into passed json filename"""
    
    with open(filename, 'w') as file:
        json.dump(json_data, file)