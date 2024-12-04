import xmltodict
import json
from typing import Dict

def read_as_dict(xml_path : str) -> Dict:
  with open(xml_path, 'r') as f:
      return xmltodict.parse(f.read())
  
def to_json(xml_path : str, json_target : str) -> None:
  with open(json_target, 'w') as f:
      f.write(json.dumps(read_as_dict(xml_path), indent=4))