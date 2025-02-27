import os
import pandas as pd
import json
import os.path
# import entities.slot 
# from entities.lector import LectorCSV, LectorJSON, LectorTXT, Lector
# from entities.aeropuerto import Aeropuerto
import datetime as dt 
from datetime import datetime
'''--------------------------'''
from unittest import TestCase
from pandas._testing import assert_series_equal

from unittest import TestCase
import sys
sys.path.append('..')
from pandas._testing import assert_frame_equal

from unittest import TestCase
from datetime import datetime, timedelta



class Slot:
    def __init__(self):
        self.id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, id, fecha_llegada, fecha_despegue):
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def slot_esta_libre_fecha_determinada(self, fecha):
        time_to_wait = dt.timedelta(0) 
        if self.fecha_final is not None: 
            time_to_wait = max(self.fecha_final - fecha, dt.timedelta(0))
        return time_to_wait




class Lector:
    def __init__(self, path: str):
        self.path = path

    def get_extention(self):
        the_extention = os.path.splitext(self.path)[-1]
        return the_extention

    def _comprueba_extension(self):
        valid_extentions = ['.csv', '.txt', '.json']
        extention = self.get_extention()
        if extention not in valid_extentions:
            raise ValueError('Archivo no tiene la extencion correcta')
        return True
    

    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(list_dicts: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(list_dicts)
        return df
    
    @staticmethod
    def converter_time_to_datetime(df_vuelos: pd.DataFrame, datetime_columns: list[str] = None) -> pd.DataFrame:
        '''
        Convierte las columnas especificadas al formato de fecha y hora si están presentes en el DataFrame.

        :param df_vuelos: DataFrame que contiene los datos
        :param datetime_columns: Lista de columnas para convertir al formato de fecha y hora
        :return: DataFrame con columnas convertidas
        '''
        if datetime_columns:
            for column in datetime_columns:
                if column in df_vuelos.columns:
                    df_vuelos[column] = pd.to_datetime(df_vuelos[column])
        return df_vuelos
    




class LectorCSV(Lector):
    '''
    He quitado el metodo __init__ por que se esta repetiendo en todos los clases-hija, 
    y creo que no hace falta implementarlo si es igual al de la clase-madre, por que igualmente esta clase se lo hereda
    Y el metodo lee_archivo() es diferente por eso lo estoy implementando aqui de diferente manera
    '''
    def lee_archivo(self):
        df_vuelos = None
        if self._comprueba_extension() and self.get_extention() == '.csv':
            df_vuelos = pd.read_csv(self.path)
            return df_vuelos
        else:
            raise ValueError("Extension de archivo incorrecta. Se esperaba '.csv'")
    
    def get_df_to_work(self):
        df_vuelos = self.lee_archivo()
        df_vuelos_with_datetime = Lector.converter_time_to_datetime(df_vuelos, ["fecha_llegada", "fecha_salida"])
        return df_vuelos_with_datetime


class LectorJSON(Lector):
    '''
    He quitado el metodo __init__ por que se esta repetiendo en todos los clases-hija, 
    y creo que no hace falta implementarlo si es igual al de la clase-madre, por que igualmente esta clase se lo hereda
    Y el metodo lee_archivo() es diferente por eso lo estoy implementando aqui de diferente manera
    '''


    def lee_archivo(self) -> list[dict]:
        if self._comprueba_extension() and self.get_extention() == '.json':
            with open(self.path, 'r', encoding='utf-8') as file:
                list_dicts = json.load(file)
            return list_dicts
        else:
            raise ValueError("Extension de archivo incorrecta. Se esperaba '.json'")
    

    def get_df_to_work(self):
        list_dicts = self.lee_archivo()
        df_vuelos = Lector.convierte_dict_a_csv(list_dicts)
        df_vuelos_with_datetime = Lector.converter_time_to_datetime(df_vuelos, ["fecha_llegada", "fecha_salida"])
        return df_vuelos_with_datetime


class LectorTXT(Lector):
    '''
    Aqui tambien he quitado el metodo __init__ por que se esta repetiendo en todos los clases-hija, 
    y creo que no hace falta implementarlo si es igual al de la clase-madre y no lo reecribo, por que igualmente esta clase se lo hereda
    Y el metodo lee_archivo() es diferente por eso lo estoy implementando aqui de diferente manera
    '''

    def lee_archivo(self):
        list_dicts = None
        if super()._comprueba_extension() and self.get_extention() == '.txt':
            with open(self.path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                keys = lines[0].rstrip().split(', ')
                list_dicts = [dict(zip(keys, line.strip().split(', '))) for line in lines[1:]]
        return list_dicts
    
    def get_df_to_work(self):
        df_vuelos = Lector.convierte_dict_a_csv(self.lee_archivo())
        df_vuelos_with_datetime = Lector.converter_time_to_datetime(df_vuelos, ["fecha_llegada", "fecha_salida"])
        return df_vuelos_with_datetime


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

    
# comprobamos la clase del aeropuerto con el tes del aeropuerto

class TestAeropuerto(TestCase):
    def setUp(self):
        vuelos = pd.DataFrame({
            'id': ['VY4548', 'VY3887', 'VY1603', 'VY3302', 'VY1121'],
            'fecha_llegada': ['2022-08-06 10:30:00', '2022-08-05 09:00:00', '2022-08-05 08:45:00',
                              '2022-08-05 08:30:00', '2022-08-06 10:15:00'],
            'retraso': ['00:10', '00:10', '-', '00:15', '-'],
            'tipo_vuelo': ['NAT', 'NAT', 'INTERNAT', 'NAT', 'NAT'],
            'destino': ['Helsinki', 'Sevilla', 'Nueva York', 'Bruselas', 'Paris']
        })

        vuelos['fecha_llegada'] = pd.to_datetime(vuelos['fecha_llegada'])

        n_slots = 2
        t_embarque_nat = 60
        t_embarque_internat = 100

        self.aeropuerto = Aeropuerto(vuelos, n_slots, t_embarque_nat, t_embarque_internat)

    def test_calcula_fecha_despegue(self):
        expected_fecha_despegue = pd.to_datetime('2022-08-06 11:30:10')  # Обновляем ожидаемую дату
        vuelo = pd.Series({
            'id': 'VY4548',
            'fecha_llegada': pd.to_datetime('2022-08-06 10:30:00'),
            'retraso': '00:10',
            'tipo_vuelo': 'NAT',
            'destino': 'Helsinki',
            'slot': 0
        })

        vuelo_calculado = self.aeropuerto.calcula_fecha_despegue(vuelo.copy())
        self.assertEqual(expected_fecha_despegue, vuelo_calculado['fecha_despegue'])

    def test_encuentra_slot(self):
        row = self.aeropuerto.df_vuelos.iloc[0]
        slot = self.aeropuerto.encuentra_slot(row['fecha_llegada'])
        self.assertEqual(1, slot)

        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        row_2 = row.copy()
        row_2['fecha_llegada'] = row['fecha_llegada'] + pd.Timedelta(minutes=30)
        slot = self.aeropuerto.encuentra_slot(row_2['fecha_llegada'])
        self.assertEqual(-1, slot)

    def test_asigna_slot(self):
        row = self.aeropuerto.df_vuelos.iloc[0].copy()
        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        row_2 = row.copy()
        row_2['fecha_llegada'] = row['fecha_llegada'] + pd.Timedelta(minutes=30)
        row_2 = self.aeropuerto.asigna_slot(row_2)

        self.assertEqual(1, row_2['slot'])
        self.assertEqual(pd.to_datetime('2022-08-06 12:40:10'), row_2['fecha_despegue'])  



# comprobamos la clase del Lector con el test del Lector

class TestLector(TestCase):
    def test_lee_archivo_csv(self):
        path = os.path.abspath('./data/vuelos_2.csv')
        expected_df = pd.DataFrame([{'id': 'VY4548', 'fecha_llegada': '2022-08-06 10:30:00', 'retraso': '-',
                                     'tipo_vuelo': 'NAT', 'destino': 'Helsinki'},
                                    {'id': 'VY3888', 'fecha_llegada': '2022-08-06 15:00:00', 'retraso': '00:10',
                                     'tipo_vuelo': 'NAT', 'destino': 'Roma'},
                                    {'id': 'VY1605', 'fecha_llegada': '2022-08-06 08:45:00', 'retraso': '-',
                                     'tipo_vuelo': 'NAT', 'destino': 'Madrid'},
                                    {'id': 'VY3307', 'fecha_llegada': '2022-08-05 12:30:00', 'retraso': '-',
                                     'tipo_vuelo': 'INTERNAT', 'destino': 'Sao Paulo'}])
        expected_df['fecha_llegada'] = pd.to_datetime(expected_df['fecha_llegada'])
        lector = LectorCSV(path)
        df = lector.get_df_to_work()
        assert_frame_equal(expected_df, df)

    def test_lee_archivo_json(self):
        path = os.path.abspath('./data/vuelos_3.json')
        expected_df = pd.DataFrame([{'id': 'VY1606', 'fecha_llegada': '2022-08-05 11:15:00', 'retraso': '-', 
                                     'tipo_vuelo': 'INTERNAT', 'destino': 'Beijing'},
                                    {'id': 'VY2650', 'fecha_llegada': '2022-08-05 20:30:00', 'retraso': '00:05', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Marrakech'},
                                    {'id': 'VY1415', 'fecha_llegada': '2022-08-05 12:10:00', 'retraso': '-', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Florencia'},
                                    {'id': 'VY6611', 'fecha_llegada': '2022-08-05 13:45:00', 'retraso': '-', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Lisboa'}])
        expected_df['fecha_llegada'] = pd.to_datetime(expected_df['fecha_llegada'])
        lector = LectorJSON(path)
        df = lector.get_df_to_work()
        assert_frame_equal(expected_df, df)

    def test_lee_archivo_txt(self):
        path = os.path.abspath('./data/vuelos_1.txt')
        expected_df = pd.DataFrame([{'id': 'VY4547', 'fecha_llegada': '2022-08-05 10:30:00', 'retraso': '-', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Paris'},
                                    {'id': 'VY3887', 'fecha_llegada': '2022-08-05 15:00:00', 'retraso': '00:10', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Sevilla'},
                                    {'id': 'VY1603', 'fecha_llegada': '2022-08-05 08:45:00', 'retraso': '-', 
                                     'tipo_vuelo': 'INTERNAT', 'destino': 'Nueva York'},
                                    {'id': 'VY3302', 'fecha_llegada': '2022-08-05 12:30:00', 'retraso': '00:15', 
                                     'tipo_vuelo': 'NAT', 'destino': 'Bruselas'}])
        expected_df['fecha_llegada'] = pd.to_datetime(expected_df['fecha_llegada'])
        lector = LectorTXT(path)
        df = lector.get_df_to_work()
        assert_frame_equal(expected_df, df)

    def test_convierte_dict_a_csv(self):
        path = os.path.abspath('./data/vuelos_1.txt')
        lector = LectorTXT(path)
        d_1 = lector.lee_archivo()
        df_1 = lector.convierte_dict_a_csv(d_1)
        self.assertIsInstance(df_1, pd.DataFrame)

        path = os.path.abspath('./data/vuelos_3.json')
        lector = LectorJSON(path)
        d_2 = lector.lee_archivo()
        df_2 = lector.convierte_dict_a_csv(d_2)
        self.assertIsInstance(df_2, pd.DataFrame)


# comprobamos la clase del Slot con el test del Slot
class TestSlot(TestCase):
    def setUp(self):
        self.vuelos = pd.DataFrame.from_dict({
            'id': {0: 'VY4548', 1: 'VY3887', 2: 'VY1603', 3: 'VY3302', 4: 'VY1121'},
            'fecha_llegada': {0: '2022-08-06 10:30:00',
                              1: '2022-08-05 15:00:00',
                              2: '2022-08-05 08:45:00',
                              3: '2022-08-05 12:30:00',
                              4: '2022-08-06 10:15:00'},
            'retraso': {0: '00:10', 1: '00:10', 2: '-', 3: '00:15', 4: '-'},
            'tipo_vuelo': {0: 'NAT', 1: 'NAT', 2: 'INTERNAT', 3: 'NAT', 4: 'NAT'},
            'destino': {0: 'Helsinki', 1: 'Sevilla', 2: 'Nueva York', 3: 'Bruselas', 4: 'Paris'}
        })
        self.vuelos['fecha_llegada'] = pd.to_datetime(self.vuelos['fecha_llegada'])
        self.slot = Slot()
        self.slot.asigna_vuelo('VY4548', datetime(2022, 8, 6, 10, 30, 0), datetime(2022, 8, 6, 11, 40, 0))

    def test_slot_esta_libre_fecha_determinada(self):
        expected_time = timedelta(minutes=30)
        d = datetime(2022, 8, 6, 11, 10, 0)
        tmp = self.slot.slot_esta_libre_fecha_determinada(d)
        self.assertEqual(expected_time, tmp)

        expected_time = timedelta(0)
        d = datetime(2022, 8, 6, 11, 50, 0)
        tmp = self.slot.slot_esta_libre_fecha_determinada(d)
        self.assertEqual(expected_time, tmp)



if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

    df = main(path_1, path_2, path_3)


    # creamos un aeropuerto
    aeropuerto = Aeropuerto(df, slots=3, t_embarque_nat=60, t_embarque_internat=100)
    
    aeropuerto.asigna_slots()
    print(aeropuerto.df_vuelos)






    


# ----------los tests----------------------------------------
    # test del aeropuerto
    import unittest
    unittest.main()

    