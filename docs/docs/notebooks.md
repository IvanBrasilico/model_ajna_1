# ChestXRay 

### notebooks na base chestXRay


#### 01-Baseline-redesimples-chestXRay
<a href="../html/01-Baseline-redesimples-chestXRay.html" 
target="_blank">01-Baseline-redesimples-chestXRay</a>

Rede convolucional bem simples treinada do zero.

Input shape = 150, 150

acc: 0.9279 - val_acc: 0.8285

#### 01b-Baseline-redesimples-chestXRay-tamanhomaior
<a href="../html/01b-Baseline-redesimples-chestXRay-tamanhomaior.html" 
target="_blank">01b-Baseline-redesimples-chestXRay-tamanhomaior</a>

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
 
Conforme previsto pela teoria, o sobreajuste aumentou. 
 
acc foi para 0.96 e val_acc caiu para menos de 0.80
 
- Quarta tentativa, com regularização L1 e L2 na última camada e otimizador Adam,
pareceu que ia conseguir melhoria, foi expandido o treinamento para 50 épocas iniciando com uma
lr maior, mas a melhoria foi apenas marginal, com val_acc ensaiando ultrapassar 0.87 mas oscilando bastante

Em 04/06/2019 o melhor modelo foi:

Epoch 14/50
acc: 0.9507 val_acc: 0.8429


Conclusões/próximos passos


- Tentar aumentar regularização, utilizar keras-tuner

- Testar modelo pré-treinado mais poderoso (TransferLearning)

- Olhar exemplos de kernel no kaggle com melhor desempenho em busca de idéias

#### 02c-TransferLearningSimples-FeatureExtractionRegularizer-chestXRay
<a href="../html/02c-TransferLearningSimplesFeatureExtractionRegularizer-chestXRay.html" 
target="_blank">02c-TransferLearningSimplesFeatureExtractionRegularizer-chestXRay</a>


Utilizar DenseNet121 como feature extraction. Treinar classificador na saída desta rede.

Resultado testes:
acc: 0.93 val_acc: 0.82

Próximo passo:
 
Gravar em .npy uma matriz com todas as features extraídas da base de treinamento e fazer 
Grid Search e Random Search do melhor classificador obtido.


#### 02d-TransferLearning-FeatureExtraction-HyperParamTuner-chestXRay
<a href="../html/02d-TransferLearningFeatureExtractionHyperParamTuner-chestXRay.html" 
target="_blank">02d-TransferLearningFeatureExtractionHyperParamTuner-chestXRay</a>

Esta rede usa como entrada uma última camada maxpooling já salva, de saída da DenseNet121 aplicada à
base de treinamento. Como todo o processamento convolucional já está realizado, o treinamento do classificador
é centenas de vezes mais rápido. Assim, facilita o tunning da camada classificadora.

Resultado: 

Foi possível obter um classificador utilizando somente a saída da DenseNet121 original com pesos da imagenet:

Base original:      acc 0.95 val_acc 0.89
recall pneumonia:       0.95         0.97



#### 02e-auxiliar-ImageAugmentation
<a href="../html/02e-auxiliar-ImageAugmentation.html" 
target="_blank">02e-auxiliar-ImageAugmentation</a>

Este notebook é apenas para gerar uma base aumentada pré-processada. Será utilizado pelo outro notebook 02e.

O objetivo é tentar diminuir o sobreajuste / distãncia entre acc e val_acc e agilizar a fase de treinamento.

#### 02e-FineTunning-chestXRay
<a href="../html/02e-FineTunning-chestXRay.html" 
target="_blank">02e-FineTunning-chestXRay</a>

Aqui está sendo treinada uma rede DenseNet121 do 02c empilhada com o classificador do 02d. 

Problemas: não ficou claro se os pesos do notebook 02d foram aproveitados. Eles são carregados, os testes dão resultado
similar ao 02d, mas quando inicia o treinamento de fine tunning os números de acc e val_acc caem próximos de 0.5,
para depois voltarem a subir, mesmo quando se utiliza uma lr extremamente baixa. 

Melhor modelo: 
Transfermodelweights02e_etapa2.02-0.66.hdf5

Base aumentada: acc 0.99 val_acc 0.83

Obs: Houve um problema, o acc na base train indica 99% no treinamento, mas estranhamente cai
para 95% no relatório. Investigar. 

Base original:      acc 0.95 val_acc 0.89
recall pneumonia:       0.96         0.97

#### Observações finais

Considero que para este tipo de problema, o mais importante é um recall alto para pneumonia.

O modelo final tem um recall excelente, embora o desejável neste caso seja 100%, não sabemos se há
erro de rotulagem nem qual o erro humano, muito menos o Bayes Error. Portanto, não dá para saber se 
é factível melhorar acima de 95-97% de recall. 

Não foi possível obter ganhos significativos em relação ao baseline com as técnicas empregadas. 
A melhoria foi marginal, de menos de 5% em relação à rede neural simples. Tabela abaixo.

REDE 01b
Accuracy:           acc 0.95 val_acc 0.85
recall pneumonia:       0.94         0.95
REDE 02e
Accuracy:           acc 0.95 val_acc 0.89
recall pneumonia:       0.96         0.97

# Vazios 

### notebooks container vazio-nvazio

#### 01-Baseline-redesimples-vazio
<a href="../html/01-Baseline-redesimples-vazio.html" 
target="_blank">01-Baseline-redesimples-vazio</a>

Rede convolucional bem simples treinada do zero.

acc: 0.9551 - val_acc: 0.9564

Este notebook também contém visualizações para tentar entender melhor o que foi aprendido pela rede.

#### 01b-Baseline-redesimples-vazio-tamanhomaior
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
    

#### 02-TransferLearningSimples-vazio
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


#### 02b-TransferLearningSimplesRegularizer-vazio
<a href="../html/02b-TransferLearningSimplesRegularizer-vazio.html" 
target="_blank">02b-TransferLearningSimplesRegularizer-vazio</a>

Rede Densenet121, pré treinada na imagenet, com regularização.

**Não houve sucesso neste treinamento, necessário debugar posteriormente** 


#### 02c-TransferLearning-FeatureExtractionRegularizer-vazio
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

### 
<a href="../html/.html" 
target="_blank"></a>

