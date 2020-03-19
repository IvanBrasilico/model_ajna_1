""""Exporta imagens e bboxes gravados em predictions para formato yolo

Extrai imagens e bouding boxes já previstas para formato YOLO
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
from PIL.Image import Image
from bson import ObjectId

from .utils import fs, mongodb, str_yesterday, str_today, parse_datas


def cursor_images_and_bboxes(db, start, end, limit):
    query = {'metadata.contentType': 'image/jpeg',
             'metadata.predictions.bbox': {'$exists': True},
             'metadata.dataescaneamento': {'$gte': start, '$lt': end}}
    projection = {'_id': 1, 'metadata.predictions.bbox': 1}
    # r = requests.post('https://ajna.labin.rf08.srf/virasana/grid_data', json=params, verify=False)
    return db.fs.files.find(query, projection).limit(limit)


MIN_RATIO = 1.8


def extract_yolo(rows: list, min_ratio=MIN_RATIO):
    """Receives a list and generates YOLO annotations.

    Receives a list of MongoDB records. Each line must have _id of the image
    and a predictions field with the bboxes

    """
    if not os.path.exists('yolo'):
        os.mkdir('yolo')
    count = 0
    for count, row in enumerate(rows):
        _id = row['_id']
        predictions = row['metadata']['predictions']
        caminho_atual = os.path.join('yolo', str(_id))
        if os.path.exists(caminho_atual):
            print(str(_id), ' existe, abortando...')
            continue
        oid = ObjectId(_id)
        if fs.exists(oid):
            grid_out = fs.get(oid)
            image = Image.open(io.BytesIO(grid_out.read()))
            xfinal, yfinal = image.size
            if xfinal / yfinal < min_ratio:
                print(image.size, ' - abortando...')
                continue
            os.mkdir(caminho_atual)
            arquivo_atual = os.path.join(caminho_atual, str(_id))
            with open(arquivo_atual + '.txt', 'w') as out_handle:
                for prediction in predictions:
                    bbox = prediction['bbox']
                    print(bbox, image.size)
                    coords = [str((bbox[1] + bbox[3]) / 2 / xfinal),
                              str((bbox[0] + bbox[2]) / 2 / yfinal),
                              str((bbox[3] - bbox[1]) / xfinal),
                              str((bbox[2] - bbox[0]) / yfinal)]
                    out_handle.write('0 ' + ' '.join(coords) + '\n')
            with open(os.path.join(caminho_atual, 'classes.txt'), 'w') as out_handle:
                out_handle.write('0 Container')
            image.save(arquivo_atual + '.jpg')
    print('%s arquivos exportados...' % count)
    return count


@click.command()
@click.option('--inicio', default=str_yesterday,
              help='Dia de início (dia/mês/ano) - padrão ontem')
@click.option('--fim', default=str_today,
              help='Dia de fim (dia/mês/ano) - padrão hoje')
@click.option('--limit', default=100,
              help='Limite de registros - padrão 100')
def do(inicio, fim, limit):
    print('Iniciando...')
    start, end = parse_datas(inicio, fim)
    print(start, end)
    s0 = time.time()
    cursor = cursor_images_and_bboxes(mongodb, start, end, limit)
    count = extract_yolo(cursor)
    s1 = time.time()
    print('{:0.2f} segundos para processar {:d} registros'.format((s1 - s0), count))
    print('Resultado salvo no diretório yolo')


if __name__ == '__main__':
    do()
