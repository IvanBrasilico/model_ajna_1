"""Funções utilitárias para exportação e montagem de training sets."""
import io
import os
from datetime import date, datetime, timedelta

from PIL import Image
from bson import ObjectId
from gridfs import GridFS
from pymongo import MongoClient

MIN_RATIO = 1.8

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

def get_image(row, crop=False, min_ratio=MIN_RATIO):
    """Retrieve image content from Mongo, crop on bbox if crop is True."""
    oid = ObjectId(row['_id'])
    if fs.exists(oid):
        grid_out = fs.get(oid)
        image = Image.open(io.BytesIO(grid_out.read()))
        xfinal, yfinal = image.size
        if xfinal / yfinal < min_ratio:
            print(image.size, ' - abortando...')
            return None
        if crop:
            coords = row['metadata']['predictions'][0]['bbox']
            image = image.crop((coords[1], coords[0], coords[3], coords[2]))
    return image


def get_cursor_filtrado(db, filtro, projection, limit=None):
    print(filtro)
    cursor = db.fs.files.find(filtro, projection).limit(limit)
    # params = {'query': filtro, 'projection': projection}
    # r = requests.post('https://ajna.labin.rf08.srf/virasana/grid_data',
    # json=params, verify=False)
    return cursor


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
