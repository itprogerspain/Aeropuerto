
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'entities')))

import pandas as pd
from entities.slot import Slot
from entities.lector import LectorCSV, LectorJSON, LectorTXT, Lector
from entities.aeropuerto import Aeropuerto


    

def preprocess_data(df_list):
    df_concat = pd.concat(df_list, ignore_index=True)
    return df_concat


def main(path_1, path_2, path_3):
    lector_txt = LectorTXT(path_1)
    lector_csv = LectorCSV(path_2)
    lector_json = LectorJSON(path_3)


    df_vuelos_1 = lector_txt.get_df_to_work()
    df_vuelos_2 = lector_csv.get_df_to_work()
    df_vuelos_3 = lector_json.get_df_to_work()

    df_list = [df_vuelos_1, df_vuelos_2, df_vuelos_3]
    df = preprocess_data(df_list)

    return df

    

if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

    df = main(path_1, path_2, path_3)


    # creamos un aeropuerto
    aeropuerto = Aeropuerto(df, slots=3, t_embarque_nat=60, t_embarque_internat=100)
    
    aeropuerto.asigna_slots()
    print(aeropuerto.df_vuelos)

    
    



    








