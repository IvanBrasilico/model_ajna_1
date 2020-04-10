### Treinando YOLO ou outro modelo de detecção de objetos

O treinamento do yolo e outros modelos de object detection é um pouco mais 
complicado do que o de outros modelos. Assim, não basta criar uma rede ou importar uma rede.

Assim, o AJNA apenas disponibiliza scripts para:

1. Montar a base de dados e prepará-la para ser 
rotulada ou ter rótulos corrigidos utilizando labelImg (scripts/bboxes_to_yolo.py).

2. Após refinamento da base, preparar para uma rede de referência escolhida. Por exemplo, para
a rede Darknet yolov3, referência de implementação https://github.com/IvanBrasilico/keras-yolo3,
 o script extracoes/yolo_prepare.py cria os arquivos necessários.
 
 
 ### Instalando YOLOv3 
 
```
(venv)$deactivate
$git clone https://github.com/IvanBrasilico/keras-yolo3
$cd keras-yolo3
$echo "yolo-venv" >> .gitignore
$python3.5 -m venv yolo-venv
$. yolo-venv/bin/activate
(yolo-venv)$hash -r
(yolo-venv)$python -m pip install --upgrade pip wheel setuptools
# As versões recomendadas são 2.1.5 e 1.6.0, incompatíveis com o cuda instalado no Labin
# Versões mais atualizdas abaixo funcionaram
(yolo-venv)$pip install keras==2.1.6 tensorflow-gpu==1.13.2 h5py Pillow matplotlib
(yolo-venv)$python convert.py yolov3.cfg ../yolo_weights/yolov3.weights model_data/yolo.h5
(yolo-venv)$python yolo_video.py --image  # Para testar detecção em uma imagem
(yolo-venv)$   # Para treinar  
```

Para maiores instruções e detalhes, consultar README do projeto keras-yolo3

 