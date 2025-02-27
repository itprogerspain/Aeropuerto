import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest import TestCase
import pandas as pd
from pandas._testing import assert_series_equal

from entities.aeropuerto import Aeropuerto


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



if __name__ == '__main__':
    import unittest
    unittest.main()