"""Gera uma base de imagens com pesos e volumes.

Exporta csv com id imagem, numero container, peso e volume
na quantidade q para o diretório out.
Para gerar arquivos para treinamento de algoritmos de aprendizagem de máquina

Usage:
    python pesovolexport.py -q 1000 -out ../pesos

    -q: quantidadade de registros a exportar.
    Se omitido, pega aleatoriamente 1.000 registros da base.

    -out: diretório de destino
    Se omitido, cria arquivo pesovolexport.csv no diretório corrente.

"""
import csv
import os
import random
from datetime import datetime

import click

ENCODE = 'latin1'

from utils import mongodb, str_yesterday, str_today, parse_datas, MIN_RATIO, get_image


N_SAMPLES = 5000


@click.command()
@click.option('--inicio', default=str_yesterday,
              help='Dia de início (dia/mês/ano) - padrão ontem')
@click.option('--fim', default=str_today,
              help='Dia de fim (dia/mês/ano) - padrão hoje')
@click.option('--limit', default=100,
              help='Limite de registros (para cada categoria) - padrão 100')
@click.option('--crop', is_flag=True,
              help='Especifique crop para recortar imagem bbox')
@click.option('--out', default='.', help='Diretório de destino')
def export(inicio, fim, limit, crop, out):
    """Exporta csv com peso e volume do contêiner.

    Consulta MongoDB exportando campos selecionados e gravando em
    arquivo csv para facilitar posterior treinamento de modelo sklearn.

    """
    print('iniciando consulta')
    start, end = parse_datas(inicio, fim)
    filtro = {'metadata.contentType': 'image/jpeg',
              'metadata.carga.container': {'$exists': True}}
    filtro['metadata.dataescaneamento'] = {'$gte': start, '$lt': end}
    cursor = mongodb['fs.files'].find(
        filtro,
        {'metadata.recintoid': 1,
         'metadata.carga.container.container': 1,
         'metadata.carga.container.taracontainer': 1,
         'metadata.carga.container.pesobrutoitem': 1,
         'metadata.carga.container.volumeitem': 1}).limit(limit * 3)

    containers = []
    for linha in cursor:
        recinto = linha['metadata']['recintoid']
        item = linha['metadata']['carga']['container']
        if item[0].get('pesobrutoitem'):
            tara = float(item[0]['taracontainer'].replace(',', '.'))
            peso = float(item[0]['pesobrutoitem'].replace(',', '.'))
            volume = float(item[0]['volumeitem'].replace(',', '.'))
            containers.append(
                [linha['_id'],
                 recinto,
                 linha['metadata']['carga']['container'][0]['container'],
                 tara, peso, volume])
        #####
        # Rever importaçao! Pelo jeito está puxando contêiner 2 vezes,
        # 1 para MBL e outra para HBL
        # peso = 0.
        # volume = 0.
        # for item in linha['metadata']['carga']['container']:
        #    if item.get('pesobrutoitem'):
        #        peso += float(item['pesobrutoitem'].replace(',', '.'))
        #        volume += float(item['volumeitem'].replace(',', '.'))
        # if peso != 0.:

    print(len(containers))

    export = [['id', 'recintoid', 'numero', 'tara', 'peso', 'volume']]
    export.extend(random.sample(containers, limit))
    with open(os.path.join(out, 'pesovolexport.csv'),
              'w', encoding=ENCODE, newline='') as out:
        writer = csv.writer(out)
        writer.writerows(export)


if __name__ == '__main__':
    export()
