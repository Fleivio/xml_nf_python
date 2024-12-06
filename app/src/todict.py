import xmltodict
import json
from lxml import etree

def read_as_dict(xml_path, xpath = None):
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
