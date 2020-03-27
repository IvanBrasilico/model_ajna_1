""""Exporta imagens com rotulo vazio ou cheio para diretorio

Extrai imagens para diretorio VAZIO OU NVAZIO de acordo com a marcação 
na base de dados.
Para permitir correções das marcações e treinamento de novos modelos


Options:
  --inicio TEXT    Dia de início (dia/mês/ano) - padrão menos 10 dias
  --fim TEXT       Dia de fim (dia/mês/ano) - padrão hoje
  --limit INTEGER  Limite de registros - padrão 100

"""
import os
import time

import click

from utils import mongodb, str_yesterday, str_today, parse_datas, MIN_RATIO, get_image, \
    get_cursor_filtrado


def cursor_vazio_nvazio(db, start, end, limit, vazio=True, crop=False):
    query = {'metadata.contentType': 'image/jpeg',
             'metadata.carga.vazio': {'$exists': True},
             'metadata.carga.vazio': vazio,
             'metadata.dataescaneamento': {'$gte': start, '$lt': end}}
    projection = {'_id': 1, 'metadata.carga.vazio': 1}
    if crop:
        query['metadata.predictions.bbox'] = {'$exists': True}
        projection['metadata.predictions.bbox'] = 1
    return get_cursor_filtrado(db, query, projection, limit)


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
    for label in (True, False):
        cursor = cursor_vazio_nvazio(mongodb, start, end, limit, label, crop)
        count = extract_to(cursor, crop)
        s1 = time.time()
        print('{:0.2f} segundos para processar {:d} registros'.format((s1 - s0), count))
    print('Resultado salvo no diretório vazios')


if __name__ == '__main__':
    do()
