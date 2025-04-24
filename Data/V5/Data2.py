import pandas as pd
import io  # Necesario para leer los datos de ejemplo como si fueran archivos

# --- PASO 1: Definir los datos CSV como strings ---
# En un escenario real, reemplazarías esto con las rutas a tus archivos:
# bc_file = 'Boundary_Conditions.csv'
# sd_file = 'Supply_Demand.csv'
# yields_file = 'Yields.csv'

bc_csv_data = """0,1,2,3,4,5,6,7,8,9,10,11
Total,Total,Total,21A,21A,21A,22B,22B,22B,23C,23C,23C
Available Capacity,Scheduled Capacity,Over/Under Capacity,Available Capacity,Scheduled Capacity,Over/Under Capacity,Available Capacity,Scheduled Capacity,Over/Under Capacity,Available Capacity,Scheduled Capacity,Over/Under Capacity
11037.0,,,5155.0,,,4000.0,,,1882.0,,
10791.0,,,5258.0,,,4000.0,,,1533.0,,
10265.0,,,5182.0,,,4000.0,,,1083.0,,
10223.0,,,4840.0,,,4000.0,,,1383.0,,
"""

sd_csv_data = """0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,Semana
21A,21A,21A,21A,22B,22B,22B,22B,22B,22B,23C,23C,23C,23C,23C,23C,
Safety Stock Target (WOS),EffectiveDemand,Total Projected Inventory Balance,Inventory Balance in excess of SST,Yielded Supply,Safety Stock Target,Safety Stock Target (WOS),EffectiveDemand,Total Projected Inventory Balance,Inventory Balance in excess of SST,Yielded Supply,Safety Stock Target,Safety Stock Target (WOS),EffectiveDemand,Total Projected Inventory Balance,Inventory Balance in excess of SST,
0.0,0.0,141337199.35999998,0.0,0.0,0.0,0.0,0.0,164824302.72,0.0,0.0,0.0,0.0,0.0,184132359.936,0.0,
1.82,3920865476.2527657,-398900228.9237671,-1078892899.4955273,1694268282.3394976,283186617.3041231,1.561,1541047872.0,318044713.0594976,34858095.75537443,6610182393.901104,706503770.3388937,1.42,4705495605.907281,2088819147.929823,1382315377.590929,1.0
1.82,3920865476.2527657,-398900228.9237671,-1078892899.4955273,1694268282.3394976,283186617.3041231,1.561,1541047872.0,318044713.0594976,34858095.75537443,6610182393.901104,706503770.3388937,1.42,4705495605.907281,2088819147.929823,1382315377.590929,2.0
1.82,3920865476.2527657,-398900228.9237671,-1078892899.4955273,1694268282.3394976,283186617.3041231,1.561,1541047872.0,318044713.0594976,34858095.75537443,6610182393.901104,706503770.3388937,1.42,4705495605.907281,2088819147.929823,1382315377.590929,3.0
"""

yields_csv_data = """0,1,2,3
Product ID,21A,22B,23C
,Yield,Yield,Yield
02-28-95,0.9058,0.9084,0.9055
03-07-95,0.9058,0.9085,0.9055
03-14-95,0.9059,0.9085,0.9055000000000001
03-21-95,0.9059,0.908,0.9052
"""

# --- PASO 2: Cargar los datos CSV usando Pandas ---
# Se usa header=[1, 2] para capturar las dos filas de encabezados correctamente.
# Se usa io.StringIO para leer los strings definidos arriba como si fueran archivos.
# Reemplaza io.StringIO(xxx_csv_data) con xxx_file si lees desde archivos reales.
try:
    # Carga Boundary Conditions
    # El encabezado está en las filas 1 y 2 (índice 0-based: 1 y 2)
    bc_df = pd.read_csv(io.StringIO(bc_csv_data), header=[1, 2])

    # Carga Supply Demand
    # El encabezado está en las filas 1 y 2
    sd_df = pd.read_csv(io.StringIO(sd_csv_data), header=[1, 2])

    # Carga Yields (Aunque no se usa directamente en el formato final solicitado,
    # se carga por si fuera necesario en el futuro o para análisis)
    # El encabezado está en las filas 1 y 2
    yields_df = pd.read_csv(io.StringIO(yields_csv_data), header=[1, 2])

    # --- Limpieza Opcional de Nombres de Columna (eliminar espacios extra) ---
    # Esto puede ser útil si los nombres tienen espacios inconsistentes
    bc_df.columns = bc_df.columns.map(lambda x: tuple(str(i).strip() for i in x))
    sd_df.columns = sd_df.columns.map(lambda x: tuple(str(i).strip() for i in x))
    yields_df.columns = yields_df.columns.map(lambda x: tuple(str(i).strip() for i in x))

    # print("Columnas Boundary Conditions:")
    # print(bc_df.columns)
    # print("\nColumnas Supply Demand:")
    # print(sd_df.columns)
    # print("\nColumnas Yields:")
    # print(yields_df.columns)


except FileNotFoundError as e:
    print(f"Error CRÍTICO: Archivo no encontrado - {e}. Verifica las rutas.")
    # Podrías añadir aquí un logging más detallado o notificación
    exit()  # Detiene la ejecución si un archivo falta
except Exception as e:
    print(f"Error CRÍTICO al leer los archivos CSV: {e}. Verifica la estructura de los archivos.")
    # Podrías añadir aquí un logging más detallado o notificación
    exit()  # Detiene la ejecución en caso de error de lectura/parseo

# --- PASO 3: Determinar el número de períodos ---
# Usaremos el archivo Supply_Demand como referencia, ya que tiene la columna 'Semana'.
# La primera fila de datos (índice 0 en el DataFrame leído) parece ser un estado inicial.
# Los períodos reales parecen comenzar desde la segunda fila (índice 1).
# Contamos cuántas filas hay desde el índice 1 en adelante.

# Identificar la columna 'Semana' correctamente (puede tener un nombre de nivel superior generado automáticamente)
try:
    semana_col_level0 = sd_df.columns[-1][0]  # Nombre nivel superior de la última columna
    semana_col_level1 = sd_df.columns[-1][1]  # Nombre nivel inferior ('Semana')

    # Extraer la serie de 'Semana', omitiendo la primera fila (estado inicial)
    semana_series = sd_df[(semana_col_level0, semana_col_level1)].iloc[1:].reset_index(drop=True)

    # Convertir a número y luego a entero para obtener los números de período
    periodos = pd.to_numeric(semana_series, errors='coerce').fillna(0).astype(int)

    # El número de períodos es la longitud de esta serie
    num_periods = len(periodos)

    if num_periods == 0:
        print("Advertencia: No se encontraron datos de períodos válidos en Supply_Demand.csv (columna Semana).")
        # Decide si continuar con 0 períodos o detenerse
        # exit()

except (IndexError, KeyError) as e:
    print(f"Error CRÍTICO: No se pudo encontrar o procesar la columna 'Semana' en Supply_Demand.csv: {e}")
    print("Asegúrate de que la columna 'Semana' exista y esté en la última posición.")
    exit()

# Determinar la longitud mínima de datos disponibles en los otros archivos
# para asegurar la alineación. Los datos en bc_df también empiezan después de las cabeceras.
num_periods_bc = len(bc_df)
# num_periods_yields = len(yields_df) # No es estrictamente necesario para el cálculo actual

# Usar el mínimo número de períodos disponibles entre los archivos relevantes
# (considerando que los datos empiezan en la misma fila relativa en cada archivo)
# En este caso, Supply_Demand (quitando la fila inicial) y Boundary_Conditions
num_periods = min(num_periods, num_periods_bc)

if num_periods == 0:
    print("Error CRÍTICO: No hay suficientes datos alineados entre los archivos para generar el reporte.")
    exit()

print(f"Se procesarán {num_periods} períodos basados en los datos disponibles.")

# --- PASO 4: Extraer y Calcular los datos para el archivo final ---

output_data = {}

# 1. Periodo: Usar los números de período calculados de 'Semana'
output_data['Periodo'] = periodos[:num_periods]  # Asegurar que no exceda num_periods

# 2. Produccion: Usar 'Total Available Capacity' de Boundary_Conditions
# Acceder usando la tupla del multi-índice: ('Total', 'Available Capacity')
# Tomar las primeras `num_periods` filas de datos.
try:
    produccion_series = bc_df[('Total', 'Available Capacity')].iloc[:num_periods]
    # Convertir a numérico, reemplazando errores (ej. celdas vacías) con 0
    output_data['Produccion'] = pd.to_numeric(produccion_series, errors='coerce').fillna(0).reset_index(drop=True)
except KeyError:
    print("Error CRÍTICO: No se encontró la columna ('Total', 'Available Capacity') en Boundary_Conditions.csv.")
    exit()

# 3. Stock_Final: Suma de 'Total Projected Inventory Balance' para 21A, 22B, 23C de Supply_Demand
# Omitir la primera fila (índice 0) y tomar las siguientes `num_periods` filas.
try:
    stock_21A = pd.to_numeric(sd_df[('21A', 'Total Projected Inventory Balance')].iloc[1: 1 + num_periods],
                              errors='coerce').fillna(0)
    stock_22B = pd.to_numeric(sd_df[('22B', 'Total Projected Inventory Balance')].iloc[1: 1 + num_periods],
                              errors='coerce').fillna(0)
    stock_23C = pd.to_numeric(sd_df[('23C', 'Total Projected Inventory Balance')].iloc[1: 1 + num_periods],
                              errors='coerce').fillna(0)
    output_data['Stock_Final'] = (stock_21A + stock_22B + stock_23C).reset_index(drop=True)
except KeyError as e:
    print(
        f"Error CRÍTICO: No se encontró una columna 'Total Projected Inventory Balance' requerida en Supply_Demand.csv: {e}")
    exit()

# 4. Demanda: Suma de 'EffectiveDemand' para 21A, 22B, 23C de Supply_Demand
# Omitir la primera fila (índice 0) y tomar las siguientes `num_periods` filas.
try:
    demanda_21A = pd.to_numeric(sd_df[('21A', 'EffectiveDemand')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    demanda_22B = pd.to_numeric(sd_df[('22B', 'EffectiveDemand')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    demanda_23C = pd.to_numeric(sd_df[('23C', 'EffectiveDemand')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    output_data['Demanda'] = (demanda_21A + demanda_22B + demanda_23C).reset_index(drop=True)
except KeyError as e:
    print(f"Error CRÍTICO: No se encontró una columna 'EffectiveDemand' requerida en Supply_Demand.csv: {e}")
    exit()

# 5. Stock_Seguridad: Suma de 'Safety Stock Target' (el que NO es WOS) para 21A, 22B, 23C de Supply_Demand
# Omitir la primera fila (índice 0) y tomar las siguientes `num_periods` filas.
try:
    # ¡IMPORTANTE! Asegúrate de seleccionar la columna correcta de 'Safety Stock Target'.
    # Basado en el orden del ejemplo, parece ser la columna con índice 5, 11, y 17 (0-based)
    # O más seguro, por nombre ('<Producto>', 'Safety Stock Target')
    ss_21A = pd.to_numeric(sd_df[('21A', 'Safety Stock Target')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    ss_22B = pd.to_numeric(sd_df[('22B', 'Safety Stock Target')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    ss_23C = pd.to_numeric(sd_df[('23C', 'Safety Stock Target')].iloc[1: 1 + num_periods], errors='coerce').fillna(0)
    output_data['Stock_Seguridad'] = (ss_21A + ss_22B + ss_23C).reset_index(drop=True)
except KeyError as e:
    print(f"Error CRÍTICO: No se encontró una columna 'Safety Stock Target' requerida en Supply_Demand.csv: {e}")
    print("Verifica que el nombre sea exacto ('Safety Stock Target' y no la versión WOS).")
    exit()

# --- PASO 5: Crear el DataFrame Final ---
try:
    final_df = pd.DataFrame(output_data)

    # Asegurar que todas las columnas tengan la misma longitud (num_periods)
    # Esto debería ser manejado por los slices [:num_periods] y reset_index()
    if not all(len(col) == num_periods for col in output_data.values()):
        print("Error CRÍTICO: Las columnas calculadas tienen longitudes inconsistentes.")
        # Imprimir longitudes para depuración
        for name, col in output_data.items():
            print(f" - Columna '{name}': Longitud {len(col)}")
        exit()

except ValueError as e:
    print(f"Error CRÍTICO al crear el DataFrame final: {e}")
    print("Esto usualmente ocurre si las columnas tienen diferente número de filas.")
    exit()

# --- PASO 6: Guardar el resultado en un nuevo archivo CSV ---
output_filename = 'output_consolidado.csv'
try:
    # Usar float_format para controlar la precisión de los números decimales
    final_df.to_csv(output_filename, index=False, float_format='%.2f')
    print(f"Archivo '{output_filename}' generado exitosamente con {len(final_df)} periodos.")
    print("Por favor, revisa el archivo generado para asegurar la integridad de los datos.")

except Exception as e:
    print(f"Error CRÍTICO al guardar el archivo CSV '{output_filename}': {e}")
    # Podrías intentar guardar con otro nombre o ruta como fallback

# --- PASO 7: Mostrar un resumen (opcional) ---
print("\nVista previa de las primeras filas del resultado:")
# Usamos to_string para evitar truncamiento y ver mejor los datos
print(final_df.head().to_string(float_format='%.2f'))

print("\nVista previa de las últimas filas del resultado:")
print(final_df.tail().to_string(float_format='%.2f'))