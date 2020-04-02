import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from pickle import dump
from utils import salva_modelo


def treina_rede():
    df = pd.read_csv('log_game.csv', sep=';')

    X = df[['pos_inicial_bola', 'vento']]
    Y = df[['pos_final_bola']]

    scaler_y, scaler_x = MinMaxScaler().fit(Y), MinMaxScaler().fit(X)

    X = scaler_x.transform(X)
    Y = scaler_y.transform(Y)

    modelo = Sequential()
    modelo.add(Dense(300, input_dim=2, activation='relu'))
    modelo.add(Dense(150, activation='relu'))
    modelo.add(Dense(1, activation='relu'))
    modelo.compile(loss='mean_absolute_error', optimizer='adam')

    modelo.fit(X, Y, epochs=1000, batch_size=100)

    salva_modelo(modelo, scaler_x, scaler_y)
    
if __name__ == '__main__':
    treina_rede()