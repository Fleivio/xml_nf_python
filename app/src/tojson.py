import xmltodict
import json

def read_as_dict(xml_path):
  with open(xml_path, 'r') as f:
      return xmltodict.parse(f.read())
  
def to_json(xml_path, json_target):
  with open(json_target, 'w') as f:
      f.write(json.dumps(read_as_dict(xml_path), indent=4))