from flask import Blueprint, render_template
import os
from app.src.tojson import read_as_dict

main = Blueprint('main', __name__)

nf_directory = 'nfs'

@main.route('/')
def home():
    notas = os.listdir(nf_directory)

    dict_objs = list(map(lambda x: read_as_dict(f'{nf_directory}/{x}'), notas))
    print(dict_objs)

    return render_template('index.html', notas = dict_objs)

@main.route('/nfs/<nfe>')
def nf_view(nfe):
    nf_name = f'{nf_directory}/{nfe}'
    emissao = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/emit')[0]
    destinatario = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/dest')[0]
    entrega = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/entrega')[0]
    prods = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/det')
    tributacao = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/total/ICMSTot')[0]
    transportadora = read_as_dict(nf_name, '/nfeProc/NFe/infNFe/transp/transporta')[0]

    print(prods)

    return render_template('nf.html',
                            emissao=emissao,
                            destinatario=destinatario,
                            entrega=entrega,
                            tributacao=tributacao,
                            transportadora=transportadora,
                            prods = prods)