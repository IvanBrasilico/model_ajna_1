# Notebooks


## 01-Baseline-redesimples-vazio
<a href="/html/01b-Baseline-redesimples-vazio.html" 
target="_blank">01b-Baseline-redesimples-vazio</a>

Rede convolucional bem simples treinada do zero.

## 01b-Baseline-redesimples-vazio-tamanhomaior
<a href="/html/01b-Baseline-redesimples-vazio-tamanhomaior.html" 
target="_blank">01b-Baseline-redesimples-vazio-tamanhomaior</a>

Mesma rede convolucional, mas treinada com entrada maior (224x224). 
O tamanho de entrada é o mesmo da maioria dos modelos treinados na imagenet.


## 02-TransferLearningSimples-vazio
<a href="/html/02-TransferLearningSimples-vazio.html" 
target="_blank">02-TransferLearningSimples-vazio</a>

Rede Densenet, pré treinada na imagenet.

acc: 0.9545 - val_acc: 0.7126

Claramente, houve um sobreajuste muito grande. Os erros de classificação cometidos são gritantes.



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
pareceu que ia conseguir melhoria, foi expandido o treinamento para 50 épocas, mas
a melhoria foi apenas marginal, com val_acc ensaiando ultrapassar 0.84

Conclusões/próximos passos

- Testar modelo pré-treinado mais poderoso (TransferLearning)

- Olhar exemplos de kernel no kagle com melhor desempenho em busca de idéias


