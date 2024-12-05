import xmltodict
import json
from lxml import etree
from typing import Dict

def read_as_dict(xml_path : str, xpath = None) -> Dict:
  with open(xml_path, 'r') as f:
      
      if xpath:
        xml = etree.parse(f)
        xml = xml.xpath(xpath)

        dc = []

        for i in range(len(xml)):
          dc.append(xmltodict.parse(etree.tostring(xml[i])))
          dc[i]['_path'] = xml_path
        
        return dc

      else:
        dc = xmltodict.parse(f.read())
        dc['_path'] = xml_path
        return dc

  
def to_json(xml_path : str, json_target : str) -> None:
  with open(json_target, 'w') as f:
      f.write(json.dumps(read_as_dict(xml_path), indent=4))