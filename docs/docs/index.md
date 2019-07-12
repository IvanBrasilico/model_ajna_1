# Visão computacional com Redes Convolucionais
 
## Classificação, busca, simillaridade, reutilização de extração de características

### **Nota para a visualização em PDF** 

O site [https://ivanbrasilico.github.io/projeto/](https://ivanbrasilico.github.io/projeto/) permite uma
melhor navegação e visualização mais completa, incluindo cópia HTML de todos os notebooks.
 
O código-fonte completo do projeto está no GitHub:

[https://github.com/IvanBrasilico/projeto](https://github.com/IvanBrasilico/projeto ) 


## Introdução


Nestes documentos estão centralizadas as anotações e histórico detalhado do treinamento e testes
de alguns modelos de visão computacional.

Serão avaliadas as mesmas técnicas em bases diferentes, para efeito de comparação. 

Linhas gerais:

* Baixar a base <a href="https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia" target="_blank">chestXRay</a> 
* Gerar e baixar base de Vazios e NcmsUnicos projeto <a href="https://ivanbrasilico.github.io/ajna_docs">AJNA</a> 
* Rodar treinamento e testes com modelo convolucional simples
* Rodar treinamento e testes com modelo "State of the Art" - Pesos do Imagenet
* Rodar treinamento e testes de extração de características para classificação
* Fazer teste de extração de características para busca de similaridade
* Rodar treinamento e testes usando redes siamesas
* Fazer teste de extração de características com redes siamesas para busca de similaridade
* Autoencoders, clusterização,  para busca


## Organização

* Proposta do projeto - <a href="../html/CapstoneProject.html" target="_blank">Capstone Proposal</a>
* [Relatório resumido](resumo.md)
* Relatório com detalhes da exploração de dados, modelos desenvolvidos, testes e iterações 
* [Conclusões finais](conclusao.md)
* <a href="https://github.com/IvanBrasilico/projeto" target="_blank">Código Fonte do Projeto</a>

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
sofisticados com transfer learning, e redes siamesas. As bases utilizadas serão chestXRay, vazios e ncmsunicos.

Além da tarefa de classificação, o objetivo do projeto é tentar, com reaproveitamento, reutilizar artefatos obtidos em 
novas classificações e também validar o uso para agrupamento e similaridade. Assim, será possível economizar recurso
computacional e humano em um ambiente de produção.

Adicionalmente, uma tendência atual da IA é a busca de "Sistemas de Inteligência Aumentada", ou IA "Centauro".
Assim, os algoritmos são utilizados para empoderar operadores humanos. Com isso, além da classificação, prover agrupamento
e busca de casos similares pode aumentar o poder de operadores humanos. Como exemplo, um médico pode procurar pacientes com
casos similares para comparar prontuários e tratamentos, ou um analista de risco pode buscar imagens de escaneamento similares
no rastro de uma fraude.
