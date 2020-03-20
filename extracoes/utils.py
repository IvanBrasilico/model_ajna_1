"""Funções utilitárias para exportação e montagem de training sets."""
import os
from datetime import date, datetime, timedelta

from gridfs import GridFS
from pymongo import MongoClient

today = date.today()
str_today = datetime.strftime(today, '%d/%m/%Y')
yesterday = today - timedelta(days=1)
str_yesterday = datetime.strftime(yesterday, '%d/%m/%Y')

MONGODB_URI = os.environ.get('MONGODB_URI')
if MONGODB_URI:
    DATABASE = ''.join(MONGODB_URI.rsplit('/')[-1:])
else:
    DATABASE = 'test'

conn = MongoClient(host=MONGODB_URI)
mongodb = conn[DATABASE]
fs = GridFS(mongodb)


def parse_datas(inicio, fim):
    return datetime.strptime(inicio, '%d/%m/%Y'), \
           datetime.strptime(fim + ' 23:59:59', '%d/%m/%Y %H:%M:%S')


def campos_mongo_para_lista(db, filtro: dict,
                            chaves: list,
                            limit=0) -> list:
    """Consulta MongoDB retornando lista.

    Args:
        db: conexão com MongoDB
        filtro:filtro a aplicar na query
        chaves: campos que serão recuperados
        limit: número de registros a limitar consulta

    Returns:
        lista contendo nomes de campo na primeira linha e valores a seguir,
        no estilo de uma planilha/csv

    """
    cursor = db['fs.files'].find(filtro).limit(limit)
    lista = []
    caminhos = [campo.split('.') for campo in chaves]
    cabecalhos = [caminho[len(caminho) - 1] for caminho in caminhos]
    lista.append(cabecalhos)
    for linha in cursor:
        registro = []
        for caminho in caminhos:
            sub = linha[caminho[0]]
            for chave in caminho[1:]:
                if isinstance(sub, list):
                    sub = sub[0]
                if sub and isinstance(sub, dict):
                    sub = sub.get(chave)
            registro.append(sub)
        lista.append(registro)
    return lista
