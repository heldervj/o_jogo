import pandas as pd
from pickle import load, dump
from keras.models import model_from_json

def salva_dados(info):
    df = pd.read_csv('log_game.csv', sep=';')
    df = df.append(pd.DataFrame([info], columns=df.columns), ignore_index=True)
    df.to_csv('log_game.csv', sep=';', index=False)

def carrega_rede():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    return loaded_model

def salva_modelo(modelo, scaler_x, scaler_y):
    modelo_json = modelo.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(modelo_json)
    modelo.save_weights("model.h5")
    dump(scaler_x, open('scaler_input.pkl', 'wb'))
    dump(scaler_y, open('scaler_output.pkl', 'wb'))

    