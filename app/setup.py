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

def setup():
  setup_validation()
  setup_prod_transformation()

