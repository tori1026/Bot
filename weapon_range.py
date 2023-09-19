
import json
import os

# Load weapon data from 'groups.json'
current_dir = os.path.dirname(os.path.abspath(__file__))
groups_json_path = os.path.join(current_dir, 'groups.json')

with open(groups_json_path, 'r', encoding='utf-8') as f:
    weapon_data = json.load(f)

def get_weapon_range(weapon_name):
    """
    Get the range information of a given weapon.
    
    Parameters:
        weapon_name (str): The name of the weapon to get the range for.
        
    Returns:
        int: The range of the weapon if found, otherwise None.
    """
    for category, details in weapon_data.items():
        if weapon_name in details['weapons']:
            return details['weapons'][weapon_name].get('range', None)
    return None
