# Relatórios da BASE ChestXRay 

## 01-Baseline-redesimples-chestXRay
<a href="../html/01-Baseline-redesimples-chestXRay.html" 
target="_blank">01-Baseline-redesimples-chestXRay</a>

Rede convolucional bem simples treinada do zero.

Input shape = 150, 150

acc: 0.9279 - val_acc: 0.8285

## 01b-Baseline-redesimples-chestXRay-tamanhomaior
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

## 02c-TransferLearningSimples-FeatureExtractionRegularizer-chestXRay
<a href="../html/02c-TransferLearningSimplesFeatureExtractionRegularizer-chestXRay.html" 
target="_blank">02c-TransferLearningSimplesFeatureExtractionRegularizer-chestXRay</a>


Utilizar DenseNet121 como feature extraction. Treinar classificador na saída desta rede.

Resultado testes:
acc: 0.93 val_acc: 0.82

Próximo passo:
 
Gravar em .npy uma matriz com todas as features extraídas da base de treinamento e fazer 
Grid Search e Random Search do melhor classificador obtido.


## 02d-TransferLearning-FeatureExtraction-HyperParamTuner-chestXRay
<a href="../html/02d-TransferLearningFeatureExtractionHyperParamTuner-chestXRay.html" 
target="_blank">02d-TransferLearningFeatureExtractionHyperParamTuner-chestXRay</a>

Esta rede usa como entrada uma última camada maxpooling já salva, de saída da DenseNet121 aplicada à
base de treinamento. Como todo o processamento convolucional já está realizado, o treinamento do classificador
é centenas de vezes mais rápido. Assim, facilita o tunning da camada classificadora.

Resultado: 

Foi possível obter um classificador utilizando somente a saída da DenseNet121 original com pesos da imagenet:

Base original:      acc 0.95 val_acc 0.89
recall pneumonia:       0.95         0.97



## 02e-auxiliar-ImageAugmentation
<a href="../html/02e-auxiliar-ImageAugmentation-chestXRay.html" 
target="_blank">02e-auxiliar-ImageAugmentation</a>

Este notebook é apenas para gerar uma base aumentada pré-processada. Será utilizado pelo outro notebook 02e.

O objetivo é tentar diminuir o sobreajuste / distãncia entre acc e val_acc e agilizar a fase de treinamento.

## 02e-FineTunning-chestXRay
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

## 03-Busca-TransferLearning-Imagenet-chestXRay 
<a href="../html/03-Busca-TransferLearning-Imagenet-chestXRay.html" 
target="_blank">03-Busca-TransferLearning-Imagenet-chestXRay</a>

Teste do uso das features extraídas de uma rede pré-treinada como hash para busca de similaridade.

Testar através de distância euclidiana se a última camada de rede neural DenseNet121 possui informação interessante
para possibilitar busca por similaridade.

Foram rodadas 1.000 simulações aleatórias de busca para vários batchs diferentes, de 512 itens para base train e 
256 itens para base. No final foram rodadas 1.000 simulações para 10 batches da base treinamento.

A avaliação foi realizada por coincidência de classe nos primeiros 10 e 20 itens e também foi realizada
avaliação visual interativa.

A avaliação visual é muito difícil, precisaria de um especialista médico para avaliar.

A avaliação por classe deu uma coincidência média de menos de 80%, considerada insuficiente. 
Também foi extraída a estatística por classe: 

0 = NORMAL 1 = PNEUMONIA

**Resultados utilizando MaxPooling**

* Acerto classe 0: 53959 de 72780 (0.74)
* Acerto classe 1: 103373 de 127220 (0.81)

**Resultados utilizando AvgPooling**

* Acerto classe 0: 55893 de 75900 (0.74)
* Acerto classe 1: 103782 de 124100 (0.84)

Assim, as *features* extraídas da rede treinada na ImageNet se mostraram insuficientes para busca.
Não obstante, podem ser um ponto de partida, para treinamento de autoencoders ou outras funções
 para gerar um hash para busca de similaridade.  


## Observações finais

Considerando que para este tipo de problema o mais importante é um recall alto para pneumonia.

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

A diferença entre treinamento e validação demonstra uma variância grande, mas pelos testes na base seria importante checar
se não se trata de um  *data mismatch*. Esta base parece ter problemas de balanceamento e também de distribuição. Como
próximo passo, seria interessante fundir todos os exemplos da base orginal (train, val, test) em uma base única e fazer um
*resample* das bases de treinamento e validação, rodando cópias destes notebooks e comparando os resultados. Além disso,
testar técnicas adicionais de *image augmentation* e balanceamento de classes (parâmetro *class weight* ou aumento de uma
categoria).

## 
<a href="../html/.html" 
target="_blank"></a>

