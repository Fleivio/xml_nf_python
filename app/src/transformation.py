from lxml import etree

def transform(xml_path: str, xsl_path: str, target_path: str):
    dom = etree.parse(xml_path)
    xslt = etree.parse(xsl_path)
    transform = etree.XSLT(xslt)
    result = transform(dom)

    with open(target_path, 'wb') as f:
        f.write(result)