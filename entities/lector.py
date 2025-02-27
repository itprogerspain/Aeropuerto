
import pandas as pd
import json
import numpy as np
import os.path

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





# '''-----------------------------------------------------------'''
# # Creamos una instancia de LectorCSV, pasamos la ruta del archivo
# lector_csv = LectorCSV('data/vuelos_2.csv')

# # Leamos el archivo y conviertimos las columnas especificadas al formato de fecha y hora
# df_vuelos_2 = lector_csv.get_df_to_work()

# # Ahora df_vuelos contiene datos del archivo con las columnas ya convertidas al formato de fecha y hora.
# print(df_vuelos_2)
# '''-----------------------------------------------------------'''
# # Creamos una instancia de LectorJSON, pase la ruta al archivo JSON
# lector_json = LectorJSON('data/vuelos_3.json')

# # Obtenemos un DataFrame con columnas de fecha convertidas
# df_vuelos_3 = lector_json.get_df_to_work()

# # Imprimimos DataFrame
# print(df_vuelos_3)
# '''-----------------------------------------------------------'''
# # Creamos una instancia de LectorTXT, pasamos la ruta al archivo
# lector_txt = LectorTXT('data/vuelos_1.txt')

# # Leemos el archivo y conviertimos las columnas especificadas al formato de fecha y hora
# df_vuelos_1 = lector_txt.get_df_to_work()

# # Ahora df_vuelos contiene datos del archivo con las columnas ya convertidas al formato de fecha y hora.
# print(df_vuelos_1)
# '''-----------------------------------------------------------'''