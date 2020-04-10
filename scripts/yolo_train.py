import os
import sys

import requests
from tqdm import tqdm


def download_with_progress(url: str, out_filename: str):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        return False
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(out_filename, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print('Erro no download!!!')
        return False
    return True


if not os.path.exists('yolo_weights/yolov3.weights'):
    print('Aguarde. Fazendo download dos pesos da yolo darknet...')
    success = download_with_progress('https://pjreddie.com/media/files/yolov3.weights',
                                     'yolo_weights/yolov3.weights')
    if not success:
        sys.exit('Não foi possível obter os pesos yolov3 da darknet!!!')

