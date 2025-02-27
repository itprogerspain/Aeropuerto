```markdown
# Aeropuerto - Sistema de gestión de slots de aeropuerto

Este proyecto es una aplicación en Python para la gestión de slots en un aeropuerto. Asigna vuelos a slots disponibles según los horarios de llegada y despegue, teniendo en cuenta el tipo de vuelo (nacional o internacional) y posibles retrasos.

---

## Descripción

El programa lee datos de vuelos desde múltiples archivos en la carpeta `data/` (formatos TXT, CSV y JSON), los combina en un único conjunto de datos y los asigna a slots. Los resultados se muestran con mensajes y una tabla actualizada de vuelos. Los datos se gestionan con `pandas.DataFrame`, y los slots con las clases `Slot` y `Aeropuerto`.

---

## Instalación

1. **Requisitos:**
   - Python 3.12 o superior
   - Bibliotecas instaladas:
     - `pandas`
     - `numpy`

2. **Instalación de dependencias:**
   Ejecuta en la terminal:
   ```bash
   pip install -r requirements.txt
   ```

3. **Estructura del proyecto:**
   ```
   Aeropuerto/
   ├── data/              # Archivos de datos de entrada
   │   ├── vuelos_1.txt
   │   ├── vuelos_2.csv
   │   ├── vuelos_3.json
   ├── entities/          # Lógica de entidades
   │   ├── __init__.py
   │   ├── aeropuerto.py  # Lógica del aeropuerto
   │   ├── lector.py      # Lógica de lectura de archivos
   ├── slot.py            # Gestión de slots
   ├── test/              # Pruebas unitarias
   │   ├── test_aeropuerto.py
   │   ├── test_lector.py
   │   ├── test_slot.py
   ├── venv/              # Entorno virtual
   ├── main.py            # Punto de entrada
   ├── requirements.txt   # Dependencias
   ├── Dockerfile         # Configuración para Docker
   ├── .dockerignore      # Archivos ignorados por Docker
   ├── test.py            # Script de pruebas (opcional)
   ├── README.md          # Documentación
   ```

---

## Uso

1. **Preparación de datos:**
   - Coloca los archivos con datos de vuelos en la carpeta `data/` con los siguientes formatos:
     - `vuelos_1.txt`: Formato de texto con columnas separadas por comas (ejemplo: `id,fecha_llegada,retraso,tipo_vuelo,destino`).
     - `vuelos_2.csv`: Archivo CSV con los mismos campos.
     - `vuelos_3.json`: Archivo JSON con una lista de diccionarios.
   - Ejemplo de contenido para `vuelos_2.csv`:
     ```
     id,fecha_llegada,retraso,tipo_vuelo,destino
     VY1603,2022-08-05 08:45:00,-,INTERNAT,Nueva York
     VY4547,2022-08-05 10:30:00,-,NAT,Paris
     ```
   - Asegúrate de que todos los archivos tengan las mismas columnas.

2. **Ejecución del programa (localmente):**
   - Asegúrate de que los archivos estén en `data/`.
   - Abre una terminal en la carpeta del proyecto.
   - Ejecuta:
     ```bash
     python main.py
     ```
   - El programa procesará los tres archivos (`vuelos_1.txt`, `vuelos_2.csv`, `vuelos_3.json`), combinará los datos y mostrará los slots asignados.

---

## Uso con Docker

Puedes ejecutar el proyecto dentro de un contenedor Docker para garantizar un entorno consistente y reproducible.

### Prerrequisitos
- Instala Docker en tu máquina: [Instrucciones de instalación](https://docs.docker.com/get-docker/).

### Construcción y ejecución del contenedor

1. **Construye la imagen Docker:**
   En la raíz del proyecto (donde está el `Dockerfile`), ejecuta:
   ```bash
   docker build -t aeropuerto:latest .
   ```
   - Esto creará una imagen Docker con el nombre `aeropuerto` y la etiqueta `latest`.

2. **Ejecuta el contenedor:**
   Una vez construida la imagen, ejecuta:
   ```bash
   docker run --rm aeropuerto:latest
   ```
   - `--rm` elimina el contenedor automáticamente después de la ejecución (útil para pruebas).
   - Si deseas montar la carpeta `data/` para actualizar los archivos de entrada dinámicamente:
     ```bash
     docker run --rm -v $(pwd)/data:/app/data aeropuerto:latest
     ```

### Notas sobre Docker
- Asegúrate de que los archivos `vuelos_1.txt`, `vuelos_2.csv` y `vuelos_3.json` estén en la carpeta `data/` antes de construir la imagen.
- El archivo `.dockerignore` evita que se copien archivos innecesarios (como `venv/`) en el contenedor.
- Si deseas usar una versión específica de la imagen, puedes cambiar `latest` por otro tag, por ejemplo:
  ```bash
  docker build -t aeropuerto:v1.0 .
  docker run --rm aeropuerto:v1.0
  ```

---

## Ejemplo de salida

Al ejecutar el programa (ya sea localmente o con Docker), obtendrás:

```
El vuelo VY1603 con fecha de llegada 2022-08-05 08:45:00 y despegue 2022-08-05 10:25:00 ha sido asignado al slot 1
Vuelo ID: VY1603 - Slot asignado: 1
El vuelo VY4547 con fecha de llegada 2022-08-05 10:30:00 y despegue 2022-08-05 11:30:00 ha sido asignado al slot 1
Vuelo ID: VY4547 - Slot asignado: 1
El vuelo VY1606 con fecha de llegada 2022-08-05 11:15:00 y despegue 2022-08-05 12:55:00 ha sido asignado al slot 2
Vuelo ID: VY1606 - Slot asignado: 2
...
        id       fecha_llegada retraso  ...     destino      fecha_despegue slot
0   VY1603 2022-08-05 08:45:00       -  ...  Nueva York 2022-08-05 10:25:00    1
1   VY4547 2022-08-05 10:30:00       -  ...       Paris 2022-08-05 11:30:00    1
2   VY1606 2022-08-05 11:15:00       -  ...     Beijing 2022-08-05 12:55:00    2
...
```

### ¿Qué significa la salida?
- **Mensajes:** Indican qué vuelo (`id`), cuándo llega (`fecha_llegada`), cuándo despega (`fecha_despegue`) y qué slot se le asignó (`slot`) para cada vuelo procesado desde los archivos en `data/`.
- **Tabla:** Un `DataFrame` final que combina datos de `vuelos_1.txt`, `vuelos_2.csv` y `vuelos_3.json`, mostrando los slots asignados.

---

## Cómo funciona el código

### Módulos principales:
1. **`entities/aeropuerto.py`**  
   - La clase `Aeropuerto` inicializa 3 slots, calcula fechas de despegue (60 minutos para vuelos nacionales, 100 minutos para internacionales) y asigna vuelos.

2. **`entities/lector.py`**  
   - Clases `Lector`, `LectorCSV`, `LectorJSON`, `LectorTXT` leen y convierten datos de los archivos en `data/` a `DataFrame`.

3. **`slot.py`**  
   - La clase `Slot` gestiona la asignación y disponibilidad de slots.

4. **`main.py`**  
   - Punto de entrada: lee datos de `vuelos_1.txt`, `vuelos_2.csv` y `vuelos_3.json`, los combina con `preprocess_data`, crea una instancia de `Aeropuerto` y ejecuta la asignación de slots.

---

## Pruebas

- En la carpeta `test/` se encuentran las pruebas unitarias. Para ejecutarlas:
  ```bash
  python -m unittest discover test
  ```
  O, si usas `test.py`:
  ```bash
  python test.py
  ```

---

## Notas

- **Fecha de despegue:** Se calcula como `fecha_llegada + tiempo_de_servicio + retraso` (60 min para `NAT`, 100 min para `INTERNAT`).
- **Slots:** Si un slot está ocupado, se busca el siguiente tiempo libre (en incrementos de 10 minutos).
- **Datos:** Asegúrate de que los archivos en `data/` tengan el formato correcto y las mismas columnas.

---

## Desarrollo

- **Agregar nuevos formatos de datos:** Crea una nueva clase en `entities/lector.py`.
- **Mejorar la lógica de slots:** Añade prioridades o reglas más complejas.

---

Si tienes dudas o quieres mejorar el proyecto, ¡abre un issue y lo resolveremos juntos! ✈️
```