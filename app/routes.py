from flask import Blueprint, render_template, jsonify
import os
from app.src.tojson import read_as_dict, to_json
from lxml import etree


main = Blueprint('main', __name__)

nf_directory = 'nfs'

def notas_path():
    names =  os.listdir(nf_directory)
    return list(map(lambda x: f'{nf_directory}/{x}', names))

@main.route('/')
def home():
    dict_objs = list(map(lambda x: read_as_dict(x), notas_path()))

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

    return render_template('nf.html',
                            emissao=emissao,
                            destinatario=destinatario,
                            entrega=entrega,
                            tributacao=tributacao,
                            transportadora=transportadora,
                            prods = prods)

@main.route('/impostos')
def impostos_totais():
    def mk_obj(path):
        trib = read_as_dict(path, '/nfeProc/NFe/infNFe/total/ICMSTot')[0]
        itens = read_as_dict(path, '/nfeProc/NFe/infNFe/det')
        return {
            'tribut': trib,
            'itens': itens
        }

    notas = list(map( lambda name: mk_obj(name), notas_path()))
    notas.sort(key=lambda x: float(x['tribut']['ICMSTot']['vTotTrib']), reverse=True)
    return render_template('impostos.html', notas = notas)


@main.route('/fornecedores')
def fornecedores():
    fornecedores = []
    cnpj_acc = []

    for p in notas_path():
        codigo = read_as_dict(p, '/nfeProc/NFe/infNFe/ide/cNF')[0]['cNF']
        emit = read_as_dict(p, '/nfeProc/NFe/infNFe/emit')[0]
        cnpj = read_as_dict(p, '/nfeProc/NFe/infNFe/emit/CNPJ')[0]['CNPJ']

        emit['notas'] = []

        if cnpj in cnpj_acc:
            for f in fornecedores:
                if f['emit']['CNPJ'] == cnpj:
                    f['notas'].append({'codigo': codigo, 'path': p})
        else:
            emit['notas'].append({'codigo': codigo, 'path': p})
            fornecedores.append(emit)
            cnpj_acc.append(cnpj)


    fornecedores.sort(key=lambda x: x['emit']['xNome'], reverse=False)


    return render_template('fornecedores.html', fornecedores = fornecedores)


@main.route('/transportadoras')
def transportadoras():
    transportadoras = []
    cnpj_acc = []

    for p in notas_path():
        codigo = read_as_dict(p, '/nfeProc/NFe/infNFe/ide/cNF')[0]['cNF']
        transp = read_as_dict(p, '/nfeProc/NFe/infNFe/transp/transporta')[0]
        cnpj = read_as_dict(p, '/nfeProc/NFe/infNFe/transp/transporta/CNPJ')[0]['CNPJ']

        transp['notas'] = []

        if cnpj in cnpj_acc:
            for t in transportadoras:
                if t['transporta']['CNPJ'] == cnpj:
                    t['notas'].append({'codigo': codigo, 'path': p})
        else:
            transp['notas'].append({'codigo': codigo, 'path': p})
            transportadoras.append(transp)
            cnpj_acc.append(cnpj)

    transportadoras.sort(key=lambda x: x['transporta']['xNome'], reverse=False)


    return render_template('transportadoras.html', transportadoras = transportadoras)

@main.route('/as_json/nfs/<nfe>')
def nf_json(nfe):
    dict = read_as_dict(f'{nf_directory}/{nfe}')
    return jsonify(dict)