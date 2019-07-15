# Visão computacional com Redes Convolucionais
 
## Classificação, busca, simillaridade, reutilização de extração de características


Ivan da Silva Brasílico

{{ git_revision_date }}
 
### **Notas para a visualização em PDF** 

O site [https://ivanbrasilico.github.io/projeto/](https://ivanbrasilico.github.io/projeto/) permite uma
melhor navegação e visualização mais completa, incluindo cópia HTML de todos os notebooks.
 
O código-fonte completo do projeto está no GitHub:

[https://github.com/IvanBrasilico/projeto](https://github.com/IvanBrasilico/projeto ) 


## Visão geral


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

## Descrição do problema e das bases

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

## Métricas

Utilizando as definições de Andrew Ng em deeplearning.ai, primeiramente tentaremos definir um erro "aceitável". Para isso,
será estimado o erro humano, em seguida será avaliado o erro de um modelo baseline e avaliados visualmente os erros cometidos.
 
Primeiramente será avaliada o acerto geral do modelo na base treinamento (accuracy), mas vigiando sempre a função custo (loss)
e também os equivalentes na base validation (val_loss e val_accuracy). Assim, primeiramente se terá como meta a redução do
"bias evitável" e ter certeza de estar com um modelo promissor. Em seguida será avaliada a variância e sobreajuste, isso é,
se o "gap" entre acc e val_acc é alto. Caso sejam, será avaliado se é um problema de sobreajuste ou um vício/erro nas bases
de dados.

Após esta primeira fase, passará a se olhar também outras métricas (precisão, recall e f1-score) de uma das classes ou
 das duas, conforme for mais importante para a visão de negócio.

Como o projeto visa permitir reaproveitamento dos artefatos gerados e também gerar índices de similaridade para busca,
serão avaliados também uso de disco, memória e velocidade de cada modelo.

Adicionalmente, para métrica de busca por similaridade, será utilizada avaliação visual pela escolha randômica de alguns
exemplos e se o rótulo é coincidente para os primeiros resultados de uma busca por similaridade.    
