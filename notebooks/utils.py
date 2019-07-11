import numpy as np
import matplotlib.pyplot as plt
import os
import random
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix


def get_imagens_erro(pgenerator, pmodel, tamanho=0):
    '''Usa generator para gerar batches.
    
    Retorna y_real e y_pred de todos os exemplos do generator E
    lista de nomes dos arquivos com erro de classificação, 
    '''
    y_local = []
    y_pred = []
    y_pred_proba = []
    X_names = []
    #  Puxando por len náo fica "preso" no loop de ImageAugmentation
    if tamanho == 0:
        tamanho = len(pgenerator)
    for i in range(tamanho):
        X_batch, y_batch = next(pgenerator)
        y_local.extend(y_batch)
        y_pred_batch = pmodel.predict_on_batch(X_batch)
        for ind, (one_pred, one_true) in enumerate(zip(y_pred_batch, y_batch)):
            # print(y, type(y))
            y_pred_proba.append(one_pred[0])
            one_pred_round = round(one_pred[0])
            y_pred.append(one_pred_round)
            if one_pred_round != one_true:
                X_names.append(pgenerator.filenames[i * pgenerator.batch_size + ind])
    return y_local, y_pred, X_names, y_pred_proba


def report(generator, y_test, y_pred):
    classes = {v:k for k, v in generator.class_indices.items()}
    print(classes)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print('R/P \t %s \t %s ' % (classes[0], classes[1]))
    print('%s \t %d \t %d' % (classes[0], tn, fp) )
    print('%s \t %d \t %d' % (classes[1], fn, tp) )
    print(classification_report(y_test, y_pred))

def report_classes(classes: dict, y_test, y_pred):
    print(classes)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print('R/P \t %s \t %s ' % (classes[0], classes[1]))
    print('%s \t %d \t %d' % (classes[0], tn, fp) )
    print('%s \t %d \t %d' % (classes[1], fn, tp) )
    print(classification_report(y_test, y_pred))

    
def plot_errors(generator, y_real, y_pred, caminho, X_names, y_pred_proba=None):
    if y_pred_proba == None:
        y_pred_proba = y_pred
    classes = {v:k for k, v in generator.class_indices.items()}
    print(classes)
    y_error = list(np.nonzero(np.array(y_real) != np.array(y_pred))[0])
    fig, ax = plt.subplots(4, 4, figsize=(16, 10))
    plt.tight_layout()
    for num_img in range(16):
        axe = ax[num_img // 4, num_img % 4]
        ind = random.randint(1, len(y_error) - 1)
        choice = y_error[ind]
        text = 'R: %s,  P: %s Proba: %s' % (classes[y_real[choice]],
                                            classes[y_pred[choice]],
                                            y_pred_proba[choice])
        axe.axis('off')
        axe.axes.get_xaxis().set_visible(False)
        axe.axes.get_yaxis().set_visible(False)
        pil_image = Image.open(os.path.join(caminho, X_names[ind]))
        axe.imshow(pil_image)
        axe.set_title(text)
