from lxml import etree

def validate_schema(xml_path, xsd_path):
  try:
    with open(xsd_path, 'rb') as xsd_file:
      schema_root = etree.XML(xsd_file.read())
      schema = etree.XMLSchema(schema_root)
    
    with open(xml_path, 'rb') as xml_file:
      xml_tree = etree.parse(xml_file)

    is_valid = schema.validate(xml_tree)
    return is_valid, schema.error_log if not is_valid else []
  except (etree.XMLSyntaxError, etree.XMLSchemaError) as e:
    return False, [str(e)]


def validate_dtd(xml_path, dtd_path):
  try:
    print("a")

    with open(dtd_path, 'rb') as dtd_file:
      dtd = etree.DTD(dtd_file)

    print("a")
    
    with open(xml_path, 'rb') as xml_file:
      xml_tree = etree.parse(xml_file)

    is_valid = dtd.validate(xml_tree)
    return is_valid, dtd.error_log if not is_valid else []
  except (etree.XMLSyntaxError, etree.DTDParseError) as e:
    return False, [str(e)]