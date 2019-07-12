# Relatórios da BASE Vazios 

## 01-Baseline-redesimples-vazio
<a href="../html/01-Baseline-redesimples-vazio.html" 
target="_blank">01-Baseline-redesimples-vazio</a>

Rede convolucional bem simples treinada do zero.

acc: 0.9551 - val_acc: 0.9564

Este notebook também contém visualizações para tentar entender melhor o que foi aprendido pela rede.

## 01b-Baseline-redesimples-vazio-tamanhomaior
<a href="../html/01b-Baseline-redesimples-vazio-tamanhomaior.html" 
target="_blank">01b-Baseline-redesimples-vazio-tamanhomaior</a>

Mesma rede convolucional, mas treinada com entrada maior (224x224). 
O tamanho de entrada é o mesmo da maioria dos modelos treinados na imagenet.

acc: 0.9589 - val_acc: 0.9616

Em 26/06/2019:

Rodada três vezes a sequência acima, 99, 101 e 103 erros de classificação 
(a mudança é devido a técnicas de image augmentation). 
Precisão de 100% na classe 0 e recall 91% ou seja 9% de erros tipo II falso negativo (predição 1 rótulo 0).

Analisando visualmente o diretório, pelo menos 25% dos erros são de rotulagem 
(os contêineres realmente não contém carga. Dos 70-75 erros restantes, 
em 20% do total o contêiner está escuro, parecendo ter carga de espuma.
 Em torno de 30% do total também há diversos tipos de ruídos na imagem,
  desde carretas que invadem a área do contêiner até borrões laterais na imagem, mas não carga.
   Então também é contêiner efetivamente vazio. Nos erros restantes (apenas 20% de 9%) 
   parece haver erro de classificação, mas o contêiner contém pouca carga.

Conclusões:

    * O erro real do algoritmo pode ser de apenas 2-4% e apenas na classe Não Vazio. 
    Este erro poderia ser melhorado com melhora no recorte do contêiner e na limpeza da imagem original.
    * Dos 9% de erros, 2% são aparentemente "fraudes": contêineres não continham carga
    * Dos 9% de erros, 2% podem ser "fraude" ou falha no escâner
    * Necessário proibir carretas que obstruam o contêiner

**O algoritmo está tentendo a ignorar cargas de contêineres declarados como vazios mas borrados/sujos ou com muito pouca carga ou com carga uniforme de espumas/materias pouco densos. Talvez fosse interessante forçar o algoritmo a ser mais tendente a diminuir este erro, mesmo que isto custasse aumento de falso positivo na classe vazio.**
    


## 01b2-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered
<a href="../html/01b2-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered.html" 
target="_blank">01b2-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered</a>

Este notebook aplica o mesmo método que 01b, mas trocando para base aumentada e filtrada 
(redução de erros de rótulo) produzida por 02c e o2d2, isto é, foi gerada nova base, já aumentada 
e excluindo erros acima e abaixo de um threshold do classificador 02c, que na inspeção visual
ficou evidente tratarem-se de erros de rotulagem, isto é, data mismatch.

Base aumentada: acc: 0.97 - val_acc: 0.97
Base original:  acc: 0.96 - val_acc: 0.96

## 01b3-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered-menostranform
<a href="../html/01b3-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered-menostransform.html" 
target="_blank">01b3-Baseline-redesimples-vazio-tamanhomaior-augmented-filtered-menostransform</a>

Este notebook aplica o mesmo método que 01b, mas trocando para base aumentada e filtrada 
(redução de erros de rótulo) produzida por 02c e o2d2, isto é, foi gerada nova base, já aumentada 
e excluindo erros acima e abaixo de um threshold do classificador 02c, que na inspeção visual
ficou evidente tratarem-se de erros de rotulagem, isto é, data mismatch.

Além disso, na inspeção visual do notebook 01b2 ficou a impressão de que os erros que ainda 
estavam ocorrendo eram: erros que mesmo o humano teria dificuldade (contêineres com espuma, por exemplo) ou
erros de rótulo persistentes. Além desses, o algoritmo ainda erra em alguns poucos casos de contêiner
contendo muito pouca carga, especialmente se esta se concentra apenas no solo (provavelmente confunde com 
imagens de vazio com solo poluído por carretas) ou somente em uma das portas (provavelmente confundindo com
reefer). Assim, neste notebook foi diminuída a amplitude das transformações de imagem aumentada para checar o resultado.

Base aumentada: acc: 0.97 - val_acc: 0.98
Base original:  acc: 0.96 - val_acc: 0.96

## 02-TransferLearningSimples-vazio
<a href="../html/02-TransferLearningSimples-vazio.html" 
target="_blank">02-TransferLearningSimples-vazio</a>

Rede Densenet121, pré treinada na imagenet.

acc: 0.9545 - val_acc: 0.7126

Claramente, houve um sobreajuste muito grande. Os erros de classificação cometidos são gritantes.

Foi realizado fine tunning do último bloco convolucional (conv5):

acc: 0.9523 - val_acc: 0.8045

Apesar dos resultados ruins na generalização, necessário explorar mais esta possibilidade.
A dificuldade pode ser devido ao bias em textura da imagenet. Note-se que esta base
é em tons de cinza, e o mais importante é a geometria. Imagenet é colorida e textura é 
importante.

ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness
https://arxiv.org/abs/1811.12231


## 02b-TransferLearningSimplesRegularizer-vazio
<a href="../html/02b-TransferLearningSimplesRegularizer-vazio.html" 
target="_blank">02b-TransferLearningSimplesRegularizer-vazio</a>

Rede Densenet121, pré treinada na imagenet, com regularização.

## 02c-TransferLearning-FeatureExtractionRegularizer-vazio
<a href="../html/02c-TransferLearningSimplesFeatureExtractionRegularizer-vazio.html" 
target="_blank">02c-TransferLearningSimplesFeatureExtractionRegularizer-vazio</a>

Rede Densenet121, pré treinada na imagenet, com regularização.

 acc: 0.9408 - val_acc: 0.9514

Neste caso, se optou por utilizar as camadas pré treinadas para feature extraction, e,
foi utilizada Max Pooling na última camada em vez de Avg Pooling.

Observações:

Após a extração das features das imagens, o treinamento do classificador é **centenas de
vezes** mais rápido. Assim, a extração separada dos features permitirá treinar vários
 classificadores, fazer grid search e cross validation, entre outros.  


Conforme demonstrado acima, há entre as imagens da classe nvazio diversos 
exemplos que parecem da classe vazio. Ou são erros de base ou são exemplos
 extremamente similares aos vazios. O aprendizado deve melhorar eliminando
  estes da base.
Será criada uma cópia da base sem esses exemplos, para testar os mesmos
 algoritmos e comparar.


## 02c2-TransferLearningFeatureExtraction-Vazio
<a href="../html/02c2-TransferLearningFeatureExtraction-Vazio.html" 
target="_blank">02c2-TransferLearningFeatureExtraction-Vazio</a>

* Extrair features para numpy com imageaugmented bem "suave" (teste 01b3) produzida por 02c e o2d2
   * Rodar com maxpool e com avgpool para poder comparar
* Rodar keras_tuner e comparar resultados com melhor resultado da rede simples

Base original maxpool:  acc: 0.9604 - val_acc: 0.9566
Base original avgpool:  acc: 0.9594 - val_acc: 0.9588


**Parece que não importa o que se tente, há um platô em torno de 0.96 para accuracy na base original.**

Com a base "limpa" de alguns erros de rotulagem, foi possível subir este platô para um pouco mais de 97%.
Como a maioria dos erros é na classe vazio, antes de prosseguir:
    * Testar neste mesmo notebook treinamento com class_weigth
    * Copiar este notebook e repetir mesmos passos na base gerada por 02d2 

O uso de class_weight 3 para a classe 0 (não vazio) causou queda marginal na accuracy total, mas distribuindo melhor
os erros, conforme tabela abaixo ( a accuracy caiu nas casas centesimais, em torno de 4 centésimos):

BASE TEST

Sem class_weight

              precision    recall  f1-score   support

         0.0       0.99      0.92      0.96      1166
         1.0       0.93      0.99      0.96      1138

Com class_weight
         
              precision    recall  f1-score   support

         0.0       0.97      0.94      0.95      1166
         1.0       0.94      0.97      0.95      1138


BASE TRAIN

Sem class_weight

              precision    recall  f1-score   support

         0.0       1.00      0.93      0.96     10494
         1.0       0.93      1.00      0.96     10306
         
Com class_weight

              precision    recall  f1-score   support

         0.0       0.98      0.95      0.96     10494
         1.0       0.95      0.98      0.96     10306



## 02c3-TransferLearningFeatureExtraction-Vazio
<a href="../html/02c2-TransferLearningFeatureExtraction-Vazio.html" 
target="_blank">02c2-TransferLearningFeatureExtraction-Vazio</a>

* Extrair features para numpy com imageaugmented bem "suave" e filtrado (mesma base que notebook 01b3)
   * Rodar com maxpool e com avgpool para poder comparar
* Rodar keras_tuner e comparar resultados com melhor resultado da rede simples

Detalhes no notebook. Resumindo, os resultados foram muito similares ao notebook 01b3:

  * aumento de 2% em accuracy em relação à base original, provavelmente pela correção de erros de rótulo
  * De resto, resultados similares ao notebook 02c2, em todas as tabelas (com o aumento de quase 2%)
  
 
## 02d-auxiliar-ImageAugmentation-Vazios
<a href="../html/02d-auxiliar-ImageAugmentation-Vazios.html" 
target="_blank">02d-auxiliar-ImageAugmentation-Vazios</a>

Notebook auxiliar para gerar uma base aumentada.


## 02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios 
<a href="../html/02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios.html" 
target="_blank">02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios</a>

Notebook auxiliar para gerar uma base aumentada com poucas transformações.

## 02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios 
<a href="../html/02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios.html" 
target="_blank">02d2-auxiliar-ImageAugmentationMenosTransfom-Vazios</a>

Notebook auxiliar para gerar uma base aumentada com poucas transformações.


## 03-Busca-TransferLearning-Imagenet-Vazios.ipynb
<a href="../html/03-Busca-TransferLearning-Imagenet-Vazios.html" 
target="_blank">03-Busca-TransferLearning-Imagenet-Vazios</a>

Teste do uso das features extraídas de uma rede pré-treinada como hash para busca de similaridade.

Métricas utilizadas:

- Dos 10 primeiros e dos 20 primeiros resultados(de um total de 512), quantos pertencem à mesma classe?

Uma tendência atual da IA é a busca de "Sistemas de Inteligência Aumentada", ou IA "Centauro".
Assim, os algoritmos são utilizados para empoderar operadores humanos. Com isso, além 

Foram rodadas 1.000 simulações aleatórias de busca para vários batchs diferentes, de 512 itens para base train e 
256 itens para base. No final foram rodadas 1.000 simulações para 10 batches da base treinamento.

A avaliação foi realizada por coincidência de classe nos primeiros 10 e 20 itens e também foi realizada
avaliação visual interativa.

A avaliação visual demonstrou precisão alta na comparação de vazios. Mas a comparação de contêineres com Carga, 
imagem com mais informação, pareceu bem mais prejudicada.

A avaliação por classe deu uma coincidência de pouco mais de 80%, considerada insuficiente. 
Também foi extraída a estatística por classe: 

0 = Não vazio 1 = Vazio

**Resultados utilizando MaxPooling**

* Acerto classe 0: 70719 de 99920 (0.71)
* Acerto classe 1: 85712 de 100080 (0.86)

**Resultados utilizando AvgPooling**

* Acerto classe 0: 79105 de 107680 (0.73)
* Acerto classe 1: 83533 de 92320 (0.90)  

Assim, as *features* extraídas da rede treinada na ImageNet se mostraram insuficientes para busca.
Não obstante, podem ser um ponto de partida, para treinamento de autoencoders ou outras funções
 para gerar um hash para busca de similaridade.  

## Observações

Os resultados da rede simples treinada do zero foram similares ao uso de rede DenseNet, 
mas a extração de features com rede pré treinada na imagenet pode ser um método universal
 base para vários classificadores, buscas e análises.
 
Assim, quando uma imagem entrar no Banco de Dados, pré extrair as features via uma rede pré treinada,
 salvando no Banco de Dados, pode servir como ponto de entrada para vários tipos de classificadores e 
 comparações, salvando memória e processamento posterior.
 
Os resultados utilizando maxpool e avgpool como extrator de características foram muito similares, com
leve vantagem para avgpool nos resultados e menor tempo de convergência. 


Os melhores resultados obtidos foram de 96% de accuracy e 96% de f1-score, sendo que a base parece ter 
em torno de 2% de erros de rotulagem. Com a base limpa, o resultado subiu a quase 98%.
Embora pela visualização haja espaço para melhora (alguns contêineres não vazios com muito pouca carga
mas facilmente identifiáveis pelo olho humano classificados como vazios), o modelo está muito próximo de um
candidato a colocação em produção. Outro ponto interessante é que foi demostrado ser possível utilizar
um classificador extremamente simples e rápido, que utiliza como ponto de entrada apenas 1024 números que
podem ser pré-extraídos das imagens pela rede DenseNet121 e ocupa apenas 14MB de RAM por batch. 

              precision    recall  f1-score   support

         0.0       0.98      0.95      0.96     10494
         1.0       0.95      0.98      0.96     10306
 


## 
<a href="../html/.html" 
target="_blank"></a>

