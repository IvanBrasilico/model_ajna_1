import os

import click

from utils import mongodb, get_image, str_yesterday, str_today, parse_datas, \
    get_cursor_filtrado

COCAINA = {'metadata.contentType': 'image/jpeg',
           'metadata.tags': 1}


def cursor_cocaina(db, start, end, limit=None, crop=True):
    filtro = COCAINA
    filtro['metadata.dataescaneamento'] = {'$gte': start, '$lt': end}
    if crop:
        filtro['metadata.predictions.bbox'] = {'$exists': True}
    projection = {'metadata.carga.ncm': 1,
                  'metadata.carga.conhecimento': 1,
                  'metadata.predictions.bbox': 1}
    return get_cursor_filtrado(db, filtro, projection, limit=limit)


def get_similar_image(conhecimento, ncms):
    """Para o treinamento, buscar imagem SEM cocaína do mesmo CE, DUE ou NCMs"""
    raise NotImplementedError()


def extract_to(path, cursor, crop=True):
    try:
        os.mkdir(path)
        os.mkdir(path + '/COCAINA')
        os.mkdir(path + '/SEMCOCAINA')
    except FileExistsError:
        pass
    for linha in cursor:
        _id = linha['_id']
        ncms = linha.get('metadata').get('carga').get('ncm')
        conhecimento = linha.get('metadata').get('carga').get('conhecimento').get('conhecimento')
        image = get_image(linha, crop=crop)
        if image:
            similar_image, similar_id = get_similar_image(conhecimento, ncms)
            sub_path = os.path.join(path, 'COCAINA')
            filename = str(_id) + '.jpg'
            image.save(os.path.join(sub_path, filename))
            del image
            sub_path = os.path.join(path, 'SEMCOCAINA')
            filename = str(similar_id) + '.jpg'
            similar_image.save(os.path.join(sub_path, filename))
            del similar_image


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
