
import datetime as dt 

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



# '''-------------------------------------------------------------'''
# slot = Slot()

# slot.asigna_vuelo('VY4548', dt.datetime(2022, 8, 6, 10, 30, 0), dt.datetime(2022, 8, 6, 11, 40, 0))

# fecha = dt.datetime(2022, 8, 6, 11, 10, 0)
# print('Tiempo de espera: ', slot.slot_esta_libre_fecha_determinada(fecha))  # Должен вернуть время ожидания
# '''-------------------------------------------------------------'''