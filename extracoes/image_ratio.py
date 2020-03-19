""""Análise do ratio de imagens por Recinto/Escâner.

Extrai e sumariza relação largura/altura de imagens agrupando por
por Recinto/Escâner para permitir a detecção de imagens que estão
sendo geradas com poucos pulsos de X-Ray/pouca informação e consequentemente
terão a qualidade prejudicada.

O script salva os resultados em um dicionário e salva dict com pickle.
Use o comando abaixo para carregar e analisar em um notebook ou outro script

with open('sizes_recinto.pickle', 'rb') as handle:
    sizes_recinto = pickle.load(handle)

Options:
  --inicio TEXT    Dia de início (dia/mês/ano) - padrão ontem
  --fim TEXT       Dia de fim (dia/mês/ano) - padrão hoje
  --limit INTEGER  Limite de registros - padrão 100

"""
import io
import pickle
import time
from collections import defaultdict

import click
from PIL import Image
from bson import ObjectId

from .utils import fs, mongodb, str_yesterday, str_today, parse_datas


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
    out_filename = 'sizes_recinto%s%s%s.pickle' % (end.year, end.month, end.day)
    s0 = time.time()
    sizes_recinto = defaultdict(list)
    query = {'metadata.contentType': 'image/jpeg',
             'metadata.recinto': {'$exists': True},
             'metadata.dataescaneamento': {'$gte': start, '$lt': end}}
    projection = {'_id': 1, 'metadata.recinto': 1}
    # r = requests.post('https://ajna.labin.rf08.srf/virasana/grid_data', json=params, verify=False)
    cursor = mongodb.fs.files.find(query, projection).limit(limit)
    for count, doc in enumerate(cursor):
        _id = doc['_id']
        oid = ObjectId(_id)
        if fs.exists(oid):
            grid_out = fs.get(oid)
            image = Image.open(io.BytesIO(grid_out.read()))
            # print(image.size)
            sizes_recinto[doc['metadata']['recinto']].append(image.size)
    s1 = time.time()
    # print(sizes_recinto)
    print('{:0.2f} segundos para processar {:d} registros'.format((s1 - s0), count))
    print('Resultado salvo em %s' % out_filename)
    with open(out_filename, 'wb') as handle:
        pickle.dump(sizes_recinto, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('sizes_recinto.pickle', 'rb') as handle:
    #    sizes_recinto = pickle.load(handle)


if __name__ == '__main__':
    do()
