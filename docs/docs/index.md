# Treinamento de modelos de visão computacional


## Abstract

Nestes documentos centralizadas as anotações e histórico detalhado do treinamento
de alguns modelos de visão computacional.

* Proposta do projeto - <a href="../html/CapstoneProject.html" target="_blank">Capstone Proposal</a>
* Detalhes dos [modelos desenvolvidos e exploração de dados](notebooks.md)
* <a href="https://github.com/IvanBrasilico/projeto" target="_blank">Código Fonte</a>


## Organização

O trabalho foi dividido em vários notebooks para melhor organização.

Estes notebooks estão com a seguinte nomenclatura

```
<número sequencial técnica/modelo><refinamento>-<descricao>-<base>
```

Ex: 

* 01 - número sequencial
* b - refinamento
* Transfer Learning - técnica
* vazios - base de dados

Assim:

01-RedeSimples-chestXRay é uma rede neural simples para classificar a base chestXRay

01-RedeSimples-vazios é uma rede neural simples para classificar a base vazios

01b-RedeSimples-vazios é a mesma rede/técnica do 01 mas com algumas modificações

## Modelos/bases

Conforme detalhado em CapstoneProject, serão treinadas redes convolucionais simples do zero, modelos 
sofisticados com transfer learning, e redes siameas. As bases utilizadas serão chestXRay, vazios e ncmsunicos.


 