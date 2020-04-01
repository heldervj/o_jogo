import numpy as np
import pandas as pd

def salva_dados(info):
    df = pd.read_csv('D:\Log_Game\log_game.csv', sep=';')
    df = df.append(pd.DataFrame([info], columns=df.columns), ignore_index=True)
    df.to_csv('D:\Log_Game\log_game.csv', sep=';', index=False)
    

def posiciona_player(pos_bola, vento, gravidade, altura):
        tempo_queda = np.sqrt(2*altura/gravidade).item()
        return pos_bola + (vento/2)*tempo_queda*tempo_queda

