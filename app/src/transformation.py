from lxml import etree

def transform(xml_path: str, xsl_path: str) -> str:
    dom = etree.parse(xml_path)
    xslt = etree.parse(xsl_path)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom