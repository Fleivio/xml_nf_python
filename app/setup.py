from app.src.tojson import to_json
from app.src.transformation import transform
from app.src.validation import validate_schema, validate_dtd

import os

nf_directory = 'nfs'

def setup():
  for nf in os.listdir(nf_directory):
    nf_path = f'{nf_directory}/{nf}'
    assert validate_schema(nf_path, 'files/nf_schema.xsd') == True
    assert validate_dtd(nf_path, 'files/nf_dtd.dtd') == True

  print("All validation tests passed.")
