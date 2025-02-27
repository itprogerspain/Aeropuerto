import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
from datetime import datetime, timedelta
import datetime as dt 
from slot import Slot
from lector import LectorCSV, LectorJSON, LectorTXT, Lector



class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        time_offset = self.tiempo_embarque_nat
        if row['tipo_vuelo'] == 'INTERNAT':
            time_offset = self.tiempo_embarque_internat

        retraso = pd.Timedelta(0)
        if row['retraso'] != '-':
            delay = datetime.strptime(row['retraso'], "%M:%S")
            retraso = pd.Timedelta(minutes=delay.minute, seconds=delay.second)

        row['fecha_despegue'] = row['fecha_llegada'] + pd.Timedelta(minutes=time_offset) + retraso
        return row
    

    def encuentra_slot(self, fecha_vuelo) -> int:
        for id, slot in self.slots.items():
            if slot.slot_esta_libre_fecha_determinada(fecha_vuelo) == dt.timedelta(0):
                return id
        return -1


    def asigna_slot(self, vuelo) -> pd.Series:
        slot = self.encuentra_slot(vuelo['fecha_llegada'])
        fecha_vuelo = vuelo['fecha_llegada']

        while slot == -1:
            fecha_vuelo += pd.Timedelta(minutes=10)
            slot = self.encuentra_slot(fecha_vuelo)

        vuelo['fecha_llegada'] = fecha_vuelo
        vuelo = self.calcula_fecha_despegue(vuelo)

        self.slots[slot].asigna_vuelo(vuelo['id'], vuelo['fecha_llegada'], vuelo['fecha_despegue'])

        print(f"El vuelo {vuelo['id']} con fecha de llegada {vuelo['fecha_llegada']} y despegue {vuelo['fecha_despegue']} ha sido asignado al slot {slot}")

        vuelo['slot'] = slot
        print(f"Vuelo ID: {vuelo['id']} - Slot asignado: {slot}")
        return vuelo

    def asigna_slots(self):
        self.df_vuelos.sort_values(by=['fecha_llegada'], inplace=True)
        self.df_vuelos.reset_index(drop=True, inplace=True)
        self.df_vuelos = self.df_vuelos.apply(self.asigna_slot, axis=1)
        

# '''---------------------------------------------------------------------------'''
# # comprobacion del codigo 

# lector_txt = LectorTXT(r'.\data\vuelos_1.txt')
# lector_csv = LectorCSV(r'./data/vuelos_2.csv')
# lector_json = LectorJSON(r'./data/vuelos_3.json')


# df_vuelos_1 = lector_txt.get_df_to_work()
# df_vuelos_2 = lector_csv.get_df_to_work()
# df_vuelos_3 = lector_json.get_df_to_work()

# df_list = [df_vuelos_1, df_vuelos_2, df_vuelos_3]

# df = pd.concat(df_list)
# print(df)

# # Creamos una instancia de Aeropuerto
# aeropuerto = Aeropuerto(df, slots=3, t_embarque_nat=60, t_embarque_internat=100)

# # Llamamos a un método cuando esté implementado
# aeropuerto.asigna_slots() 

# # Generamos el DataFrame para asegurarse de que todo esté funcionando correctamente
# print(aeropuerto.df_vuelos)  
# '''---------------------------------------------------------------------------'''





