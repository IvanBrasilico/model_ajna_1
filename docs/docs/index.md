# Visão computacional com Redes Convolucionais
 
## Classificação, busca, simillaridade, reutilização de extração de características


Ivan da Silva Brasílico

{{ git_revision_date }}
 
### **Notas para a visualização em PDF** 

O site [https://ivanbrasilico.github.io/model_ajna_1/](https://ivanbrasilico.github.io/projeto/) permite uma
melhor navegação e visualização mais completa, incluindo cópia HTML de todos os notebooks.
 
O código-fonte completo do projeto está no GitHub:

[https://github.com/IvanBrasilico/model_ajna_1](https://github.com/IvanBrasilico/projeto ) 


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
 
Primeiramente será avaliada o acerto geral do modelo na base treinamento (*accuracy*), mas vigiando sempre a função custo (*loss*)
e também os equivalentes na base validation (*val_loss* e *val_accuracy*). Assim, primeiramente se terá como meta a redução do
"bias evitável" e ter certeza de estar com um modelo promissor. Em seguida será avaliada a variância e sobreajuste, isso é,
se o "gap" entre acc e val_acc é alto. Caso sejam, será avaliado se é um problema de sobreajuste ou um vício/erro nas bases
de dados.

A *accuracy* (termo sem tradução exata para o Português exceto o neologismo acurácia, podendo ser traduzido também para exatidão)
mede de todas as previsões realizadas, a porcentagem de acertos, isto é: 

  total de previsões corretas / total de previsões

Após esta primeira fase, passará a se olhar também outras métricas (precisão, *recall* e *f1-score*) de uma das classes ou
 das duas, conforme for mais importante para a visão de negócio.

A diferença das métricas precisão e *recall* para accuracy simples necessita entendimento do conceito de falso positivo e falso negativo.
Assim, do total de exemplos da base submetidos ao modelo, podemos dividir por classe numa matriz de confusão. A matriz de confusão binária
tem a seguinte configuração(considerando que fixamos POSITIVO como a classe 1):

			        Valores reais
                    Classe 0	Classe 1
    Valores
    preditivos      
    Classe 0        TN		FN 
   
	Classe 1        FP		TP


Assim:

TP - True Positive é a quantidade de exemplos que estão rotulados na classe 1 e foram classificados na classe 1 corretamente pelo
modelo (classe 1 é, por exemplo, PNEUMONIA na nossa base chestXRay)

TN - True Negative é a quantidade de exemplos que estão rotulados na classe 0 e foram classificados na classe 0 corretamente pelo
modelo (classe 0 é, por exemplo, NORMAL na nossa base chestXRay)

FP - False Positive é a quantidade de exemplos que estão rotulados na classe 0 e foram classificados na classe 1 incorretamente pelo
modelo - seriam os "alarmes falsos", pessoas sem pneumonia que foram classificadas como contendo pneumonia.

FN - False Negative é a quantidade de exemplos que estão rotulados na classe 1 (Positivo para PNEUMONIA) e foram classificados na classe 0
 incorretamente pelo modelo - seriam pessoas com pneumonia que o nosso modelo mandaria para caso, sem tratamento e com risco à sua saúde e até 
risco de morte.

Assim, seria melhor que nossos erros fossem concentrados no tipo FP - melhor mandar um paciente saudável para o médico revisar o exame do 
que mandar o paciente doente para casa sem o médico analisar mais a fundo. Precisamos minimizar o erro FN mesmo que isso custe diminuir um 
pouco o *accuracy*. A isso chamamos *Recall* ou recuperação: percentual do total de pacientes doentes detectados. Na tabela apresentada, 
matematicamente é TP / TP + FN. Se FN = 0 *Recall* é 100%. Precisão é a quantidade de acertos quando o modelo detecta positivo na classe 1,
ou TP / TP + FP.

Note-se que caso se inverta a definição de "Positivo", o recall e precisão mudam, sendo quase trocados um pelo outro se a base é balanceada.
 Deve ser evitada esta confusão quando desta avaliação, por isso é importante deixar claro que a maximização de *recall* é para a detecção da
classe 1 - PNEUMONIA.

Normalmente, todo modelo tem algum erro, e esse erro pode ser direcionado através de técnicas como Image Augmentation, peso de classes ou mudança de threshold.
E há um *tradeoff* entre precisão e *recall*, quando um aumenta e outro diminui. Para medir o equilíbrio entre estas duas métricas, pode ser monitorado também
o f1-score, que é a média harmônica entre Precisão e *Recall* 



Como o projeto visa permitir reaproveitamento dos																																																																																																													artefatos gerados e também gerar índices de similaridade para busca,
serão avaliados também uso de disco, memória e velocidade de cada modelo.

Adicionalmente, para métrica de busca por similaridade, será utilizada avaliação visual pela escolha randômica de alguns
exemplos e se o rótulo é coincidente para os primeiros resultados de uma busca por similaridade.    
