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
from pymongo import MongoClient

from ajna_commons.conf import ENCODE
from ajna_commons.flask.conf import DATABASE, MONGODB_URI
from virasana.integracao import carga

N_SAMPLES = 5000
filtro = carga.ENCONTRADOS
filtro['metadata.dataescaneamento'] = {'$gt': datetime(
    2017, 10, 5), '$lt': datetime(2017, 10, 20)}


@click.command()
@click.option('--q', default=N_SAMPLES, help='Número de amostras (imagens)')
@click.option('--out', default='.', help='Diretório de destino')
def export(q, out):
    """Exporta csv com peso e volume do contêiner.

    Consulta MongoDB exportando campos selecionados e gravando em
    arquivo csv para facilitar posterior treinamento de modelo sklearn.

    """
    print('iniciando consulta')
    db = MongoClient(host=MONGODB_URI)[DATABASE]
    cursor = db['fs.files'].find(
        filtro,
        {'metadata.recintoid': 1,
         'metadata.carga.container.container': 1,
         'metadata.carga.container.taracontainer': 1,
         'metadata.carga.container.pesobrutoitem': 1,
         'metadata.carga.container.volumeitem': 1})

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
    export.extend(random.sample(containers, q))
    with open(os.path.join(out, 'pesovolexport.csv'),
              'w', encoding=ENCODE, newline='') as out:
        writer = csv.writer(out)
        writer.writerows(export)


if __name__ == '__main__':
    export()
