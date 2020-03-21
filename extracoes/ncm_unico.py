import os
from collections import Counter

import click

from utils import mongodb, get_image, str_yesterday, str_today, parse_datas, \
    get_cursor_filtrado

NCMUNICO = {'metadata.contentType': 'image/jpeg',
            'metadata.carga.ncm': {'$size': 1},
            'metadata.carga.container.indicadorusoparcial': {'$ne': 's'}
            }


def cursor_ncm_unico(db,
                     start, end,
                     limit=None,
                     crop=True):
    filtro = NCMUNICO
    filtro['metadata.dataescaneamento'] = {'$gte': start, '$lt': end}
    if crop:
        filtro['metadata.predictions.bbox'] = {'$exists': True}
    projection = {'metadata.carga.ncm': 1,
                  'metadata.predictions.bbox': 1}
    return get_cursor_filtrado(db, filtro, projection, limit=limit)


def extract_to(path, cursor, limitportipo=100, crop=True):
    tipo_counter = Counter()
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    for linha in cursor:
        _id = linha['_id']
        ncms = linha.get('metadata').get('carga').get('ncm')
        ncms_encontrados = set()
        for ncm in ncms:
            posicao = ncm.get('ncm')[:4]
            ncms_encontrados.add(posicao)
        if len(ncms_encontrados) == 1:  # Achou 1 e somente 1 posição ncm
            posicao = list(ncms_encontrados)[0]
            if tipo_counter[posicao] < limitportipo:
                image = get_image(linha, crop=crop)
                if image:
                    sub_path = os.path.join(path, posicao)
                    try:
                        os.mkdir(sub_path)
                    except FileExistsError:
                        pass
                    filename = str(_id) + '.jpg'
                    image.save(os.path.join(sub_path, filename))
                    del image
                    tipo_counter[posicao] += 1


@click.command()
@click.option('--inicio', default=str_yesterday,
              help='Dia de início (dia/mês/ano) - padrão ontem')
@click.option('--fim', default=str_today,
              help='Dia de fim (dia/mês/ano) - padrão hoje')
@click.option('--limit',
              help='Tamanho do lote',
              default=1000)
@click.option('--limitportipo',
              help='Limite por NCM ',
              default=20)
@click.option('--crop', is_flag=True,
              help='Especifique crop para recortar imagem bbox')
def exportaimagens(inicio, fim, limit, limitportipo, crop):
    start, end = parse_datas(inicio, fim)
    cursor = cursor_ncm_unico(mongodb,
                              start, end,
                              limit=limit,
                              crop=crop)
    extract_to('ncmsunicos', cursor, limitportipo=limitportipo)


if __name__ == '__main__':
    exportaimagens()
