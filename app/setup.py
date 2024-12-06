from app.src.transformation import transform
from app.src.validation import validate_schema, validate_dtd
from lxml import etree
import os

nf_directory = 'nfs'

def setup_validation():
  for nf in os.listdir(nf_directory):
    nf_path = f'{nf_directory}/{nf}'
    assert validate_schema(nf_path, 'files/nf_schema.xsd') == True
    assert validate_dtd(nf_path, 'files/nf_dtd.dtd') == True

  print("All validation tests passed.")


def setup_prod_transformation():
  with open('files/prods/all.xml', 'w') as all_file:
    root = etree.Element("Produtos")

    for nf in os.listdir(nf_directory):
      nf_path = f'{nf_directory}/{nf}'
      transform(nf_path, 'files/produtos.xsl', f'files/prods/{nf}')

      with open(f'files/prods/{nf}') as prod_file:
        tree = etree.parse(prod_file)
        produtos = tree.xpath("//det")

        for produto in produtos:
                root.append(produto)

    all_file.write(etree.tostring(root, pretty_print=True).decode())

def setup_ord_by_alph():
    for nf in os.listdir(nf_directory):
      nf_path = os.path.join(nf_directory, nf)
      tree = etree.parse(nf_path)
      root = tree.getroot()

      products = root.xpath("//det")
      
      products.sort(key=lambda p: p.xpath(".//xProd/text()")[0].lower())

      parent = products[0].getparent()
      for product in products:
        parent.remove(product)

      for product in products:
        parent.append(product)

      with open("./files/ord_alph/"+nf, "wb") as f:
        f.write(etree.tostring(tree, encoding="UTF-8", xml_declaration=True, pretty_print=True))

def setup_final():
  with open('files/prods/all.xml', 'r') as all_file:
    with open('nfs/01.xml', 'r') as nf_file:
      tree = etree.parse(nf_file)
      root = tree.getroot()

      products = root.xpath("//det")
      parent = products[0].getparent()

      for product in products:
        parent.remove(product)

      all_tree = etree.parse(all_file)
      all_root = all_tree.getroot()
      products = all_root.xpath("//det")

      products.sort(key=lambda p: float(p.xpath(".//vProd/text()")[0]))

      for product in products:
        parent.append(product)
      
      with open('files/final.xml', 'wb') as nf_file:
        nf_file.write(etree.tostring(tree, encoding="UTF-8", xml_declaration=True, pretty_print=True))

     
def setup():
  setup_validation()
  setup_prod_transformation()
  setup_ord_by_alph()
  setup_final()

