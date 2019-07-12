# Treinamento de modelos de visão computacional

## Documentação

Arquivo docs/site/pdf/combined.pdf ou no site:

https://ivanbrasilico.github.io/projeto/

## Instalação

É preciso ter o python versão 3 instalado na máquina. 

```
$git clone https://github.com/IvanBrasilico/projeto
$cd projeto
$python3 -m venv venv
$. venv/bin/activate
$pip install -r requirements.txt
```

Caso não tenha GPU disponível, rodar:
```
$pip uninstall tensorflow-gpu==2.0.0b1
$pip install tensorflow==2.0.0b1
```

Para rodar análises e treinamentos
```
$jupyter notebook
```

Para rodar site localmente
```
$mkdocs serve -f docs/mkdocs.yml
```

## Modelos/bases

Conforme detalhado em CapstoneProject, serão treinadas redes convolucionais simples do zero, modelos 
sofisticados com transfer learning, e redes siameas. As bases utilizadas serão chestXRay, vazios e ncmsunicos.


## Desenvolvido na RFB dentro do escopo do Sistema AJNA


Ivan da Silva Brasílico


Apresentado como Capstone Project no curso de Engenheiro de Machine Learning, Udacity.