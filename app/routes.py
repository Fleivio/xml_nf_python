from flask import Blueprint, render_template
import os
from app.src.tojson import read_as_dict

main = Blueprint('main', __name__)

nf_directory = 'nfs'

def notas_path():
    names =  os.listdir(nf_directory)
    return list(map(lambda x: f'{nf_directory}/{x}', names))

@main.route('/')
def home():
    dict_objs = list(map(lambda x: read_as_dict(x), notas_path()))
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

@main.route('/impostos')
def impostos_totais():
    tributacao = list(map( lambda name: read_as_dict(name, '/nfeProc/NFe/infNFe/total/ICMSTot')[0],
                         notas_path()))
    tributacao.sort(key=lambda x: float(x['ICMSTot']['vTotTrib']), reverse=True)
    return render_template('impostos.html', tribs = tributacao)


@main.route('/fornecedores')
def fornecedores():
    pass

@main.route('/transportadoras')
def transportadoras():
    pass