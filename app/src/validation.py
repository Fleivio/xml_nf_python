from lxml import etree
from typing import Tuple, List, Union

def validate_schema(xml_path: str, xsd_path: str) -> bool:
  try:
    with open(xsd_path, 'rb') as xsd_file:
      schema_root = etree.XML(xsd_file.read())
      schema = etree.XMLSchema(schema_root)
    
    with open(xml_path, 'rb') as xml_file:
      xml_tree = etree.parse(xml_file)

    return schema.validate(xml_tree)
  except:
    return False


def validate_dtd(xml_path: str, dtd_path : str) -> bool:
  try:
    with open(dtd_path, 'rb') as dtd_file:
      dtd = etree.DTD(dtd_file)
    
    with open(xml_path, 'rb') as xml_file:
      xml_tree = etree.parse(xml_file)

    return dtd.validate(xml_tree)
  except:
    return False