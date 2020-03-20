""""Exporta imagens com rotulo vazio ou cheio para diretorio

Extrai imagens para diretorio VAZIO OU NVAZIO de acordo com a marcação 
na base de dados.
Para permitir correções das marcações e treinamento de novos modelos


Options:
  --inicio TEXT    Dia de início (dia/mês/ano) - padrão menos 10 dias
  --fim TEXT       Dia de fim (dia/mês/ano) - padrão hoje
  --limit INTEGER  Limite de registros - padrão 100

"""
import io
import os
import time

import click
from PIL import Image
from bson import ObjectId

from utils import fs, mongodb, str_yesterday, str_today, parse_datas

MIN_RATIO = 1.8

def cursor_vazio_nvazio(db, start, end, limit, vazio=True, crop=False):
    query = {'metadata.contentType': 'image/jpeg', 
             'metadata.carga.vazio': {'$exists': True},
             'metadata.carga.vazio': vazio,
             'metadata.dataescaneamento': {'$gte': start, '$lt': end}}
    projection = {'_id': 1, 'metadata.carga.vazio': 1}
    if crop:
        query['metadata.predictions.bbox'] = {'$exists': True}
        projection['metadata.predictions.bbox'] = 1
    # r = requests.post('https://ajna.labin.rf08.srf/virasana/grid_data', json=params, verify=False)
    return db.fs.files.find(query, projection).limit(limit)


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


def extract_to(rows: list, crop=False, min_ratio=MIN_RATIO):
    """Receives a list, reads images and save to dir VAZIO or NVAZIO
    
    Receives a list of MongoDB records. Each line must have _id of the image
    and a metadata.carga.vazio boolean field
    
    If crop=True, then the record MUST have a predictions.bbox, and the image
    will be croped on predictions[0].bbox

    """
    caminho = 'vazios'
    if crop:
        caminho += '_cropped'
    if not os.path.exists(caminho):
        os.mkdir(caminho)
    for destino in ('VAZIO', 'NVAZIO'):
        if not os.path.exists(os.path.join(caminho, destino)):
            os.mkdir(os.path.join(caminho, destino))
    count = 0
    for count, row in enumerate(rows):
        _id = row['_id']
        vazio = row['metadata']['carga']['vazio']
        destino = 'VAZIO' if vazio else 'NVAZIO'
        caminho_atual = os.path.join(caminho, destino)
        arquivo_atual = os.path.join(caminho_atual, str(_id)) + '.jpg'
        if os.path.exists(arquivo_atual):
            print(str(_id), ' existe, abortando...')
            continue
        image = get_image(row, crop, min_ratio)
        if image:
            image.save(arquivo_atual)
    print('%s arquivos exportados...' % count)
    return count


@click.command()
@click.option('--inicio', default=str_yesterday,
              help='Dia de início (dia/mês/ano) - padrão ontem')
@click.option('--fim', default=str_today,
              help='Dia de fim (dia/mês/ano) - padrão hoje')
@click.option('--limit', default=100,
              help='Limite de registros (para cada categoria) - padrão 100')
@click.option('--crop', is_flag=True,
              help='Especifique crop para recortar imagem bbox')
def do(inicio, fim, limit, crop):
    print('Iniciando...')
    start, end = parse_datas(inicio, fim)
    print(start, end)
    s0 = time.time()
    for labels in (True, False):
        cursor = cursor_vazio_nvazio(mongodb, start, end, limit)
        count = extract_to(cursor, crop)
        s1 = time.time()
        print('{:0.2f} segundos para processar {:d} registros'.format((s1 - s0), count))
    print('Resultado salvo no diretório vazios')


if __name__ == '__main__':
    do()
