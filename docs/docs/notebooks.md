# Notebooks


## 01-Baseline-redesimples-vazio
<a href="/html/01-Baseline-redesimples-vazio.html" 
target="_blank">01-Baseline-redesimples-vazio</a>

Rede convolucional bem simples treinada do zero.

acc: 0.9551 - val_acc: 0.9564

Este notebook também contém visualizações para tentar entender melhor o que foi aprendido pela rede.

## 01b-Baseline-redesimples-vazio-tamanhomaior
<a href="/html/01b-Baseline-redesimples-vazio-tamanhomaior.html" 
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
    

## 02-TransferLearningSimples-vazio
<a href="/html/02-TransferLearningSimples-vazio.html" 
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
<a href="/html/02b-TransferLearningSimplesRegularizer-vazio.html" 
target="_blank">02b-TransferLearningSimplesRegularizer-vazio</a>

Rede Densenet121, pré treinada na imagenet, com regularização.

**Não houve sucesso neste treinamento, necessário debugar posteriormente** 


## 02c-TransferLearningSimplesFeatureExtractionRegularizer-vazio
<a href="/html/02c-TransferLearningSimplesFeatureExtractionRegularizer-vazio.html" 
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



## 01b-Baseline-redesimples-chestXRay-tamanhomaior
<a href="/html/01b-Baseline-redesimples-chestXRay-tamanhomaior.html" 
target="_blank">H01b-Baseline-redesimples-chestXRay-tamanhomaior</a>

Rede convolucional bem simples treinada do zero.
Treinamento em 04/09/2019:

Foram realizadas várias rodadas(sempre continuando pesos do menor val_loss anterior):
 
- A primeira com ImageAugmentation e lr=0.001, melhor acc=0.94 e melhor val_acc=0.82
Mesmo a rede sendo simples, aparenta ligeiro overfitting

- A segunda com lr=0.0001 e mais épocas para os callbacks,
 melhor acc=0.94 e melhor val_acc=0.83

- A terceira sem ImageAugmentation, com lr muito pequena.
 Embora ImageAugmentation seja uma técnica para reduzir overfitting,
 e a priori tirar possa parecer contrasenso, apenas para  
 testar se deixar a base de treinamento mais parecida com a de testes reduz erro de
 generalização, ao menos nesses exemplos e no "fine tunning"
 
 Conforme a teoria previa, o sobreajuste aumentou. acc foi para 0.96 e val_acc caiu para menos de 0.80
 
- Quarta tentativa, com regularização L1 e L2 na última camada e otimizador Adam,
pareceu que ia conseguir melhoria, foi expandido o treinamento para 50 épocas iniciando com uma
lr maior, mas a melhoria foi apenas marginal, com val_acc ensaiando ultrapassar 0.87 mas oscilando bastante

Conclusões/próximos passos


- Tentar aumentar regularização, utilizar keras-tuner

- Testar modelo pré-treinado mais poderoso (TransferLearning)

- Olhar exemplos de kernel no kaggle com melhor desempenho em busca de idéias

