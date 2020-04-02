import numpy as np
import pandas as pd
from pickle import load
from keras.models import model_from_json
from utils import carrega_rede


""" Modelagem clássica """
def modelo_classico(pos_bola, vento, gravidade, altura):

    """ Implementa o cálculo da posição final da bola, através da altura,
        gravidade, vento e a posição inicial da bola. """
    tempo_queda = np.sqrt(2*altura/gravidade).item()
    return pos_bola + (vento/2)*tempo_queda*tempo_queda

""" Rede Neural """
def rede_neural(pos_bola, vento, gravidade, altura):

    """ Utiliza a rede neural criada pelo treina_rede() 
        para calcular a posição final da bola. """
    
    modelo = carrega_rede() 
    inputs = np.array([pos_bola, vento]).reshape(1,2)
    scaler_x = load(open('scaler_input.pkl', 'rb'))
    scaler_y = load(open('scaler_output.pkl', 'rb'))
    inputs = scaler_x.transform(inputs)

    return scaler_y.inverse_transform(modelo.predict(
        inputs
    )[0][0].reshape(-1,1)).item()




def posiciona_player(modelagem, *args):
    if modelagem == 'down':
        return modelo_classico(*args)
    else:
        return rede_neural(*args)



