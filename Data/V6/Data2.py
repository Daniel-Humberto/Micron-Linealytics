import pandas as pd
import numpy as np
import os


def load_csv_data(filename):
    """
    Carga un archivo CSV y lo devuelve como texto para análisis manual
    """
    if not os.path.exists(filename):
        print(f"ADVERTENCIA: El archivo {filename} no existe en el directorio actual.")
        return None

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    return content


def process_boundary_conditions(filename='Boundary_Conditions.csv'):
    """
    Procesa el archivo Boundary_Conditions.csv respetando su estructura original
    """
    print(f"\nProcesando {filename}...")

    if not os.path.exists(filename):
        print(f"ADVERTENCIA: El archivo {filename} no existe en el directorio actual.")
        return pd.DataFrame()

    # Intenta leer el archivo como CSV directamente
    try:
        raw_data = pd.read_csv(filename, header=None)
        print(f"  - Forma del archivo raw: {raw_data.shape}")

        # Encontrar la fila donde comienzan los datos numéricos
        # Típicamente es la cuarta fila (índice 3)
        start_row = 3

        # Extraer los datos numéricos
        data_rows = raw_data.iloc[start_row:].copy()
        print(f"  - Filas de datos extraídas: {len(data_rows)}")

        # Crear DataFrame con las columnas correctas
        capacity_data = []
        for index, row in data_rows.iterrows():
            try:
                # Extraer valores de capacidad (columnas 3, 6, 9)
                capacity_row = {
                    '21A': pd.to_numeric(row[3], errors='coerce'),
                    '22B': pd.to_numeric(row[6], errors='coerce'),
                    '23C': pd.to_numeric(row[9], errors='coerce')
                }
                capacity_data.append(capacity_row)
            except Exception as e:
                print(f"  - Error al procesar fila {index} de {filename}: {e}")
                print(f"  - Contenido de la fila: {row}")
                # Usar valores por defecto si hay error
                capacity_data.append({'21A': 0.0, '22B': 0.0, '23C': 0.0})

        result_df = pd.DataFrame(capacity_data)
        print(f"  - DataFrame final: {result_df.shape}")
        return result_df

    except Exception as e:
        print(f"ERROR al procesar {filename}: {e}")
        return pd.DataFrame(columns=['21A', '22B', '23C'])


def process_supply_demand(filename='Supply_Demand.csv'):
    """
    Procesa el archivo Supply_Demand.csv respetando su estructura original
    """
    print(f"\nProcesando {filename}...")

    if not os.path.exists(filename):
        print(f"ADVERTENCIA: El archivo {filename} no existe en el directorio actual.")
        return pd.DataFrame()

    try:
        raw_data = pd.read_csv(filename, header=None)
        print(f"  - Forma del archivo raw: {raw_data.shape}")

        # La fila de datos comienza después de las cabeceras
        start_row = 3

        # Extraer filas con datos numéricos
        data_rows = raw_data.iloc[start_row:].copy()
        print(f"  - Filas de datos extraídas: {len(data_rows)}")

        # Crear DataFrame con la estructura correcta
        supply_demand_data = []
        for index, row in data_rows.iterrows():
            try:
                # Mapeo de columnas según estructura (0-based indexing)
                # 21A: columnas 1, 2, 5
                # 22B: columnas 7, 8, 11
                # 23C: columnas 13, 14, 15
                supply_demand_row = {
                    '21A_Demand': pd.to_numeric(row[1], errors='coerce'),
                    '21A_Stock': pd.to_numeric(row[2], errors='coerce'),
                    '21A_SafetyStock': pd.to_numeric(row[5], errors='coerce'),

                    '22B_Demand': pd.to_numeric(row[7], errors='coerce'),
                    '22B_Stock': pd.to_numeric(row[8], errors='coerce'),
                    '22B_SafetyStock': pd.to_numeric(row[11], errors='coerce'),

                    '23C_Demand': pd.to_numeric(row[13], errors='coerce'),
                    '23C_Stock': pd.to_numeric(row[14], errors='coerce'),
                    '23C_SafetyStock': pd.to_numeric(row[15], errors='coerce'),
                }
                supply_demand_data.append(supply_demand_row)
            except Exception as e:
                print(f"  - Error al procesar fila {index} de {filename}: {e}")
                # Usar valores por defecto si hay error
                supply_demand_data.append({
                    '21A_Demand': 0.0, '21A_Stock': 0.0, '21A_SafetyStock': 0.0,
                    '22B_Demand': 0.0, '22B_Stock': 0.0, '22B_SafetyStock': 0.0,
                    '23C_Demand': 0.0, '23C_Stock': 0.0, '23C_SafetyStock': 0.0
                })

        result_df = pd.DataFrame(supply_demand_data)
        print(f"  - DataFrame final: {result_df.shape}")
        return result_df

    except Exception as e:
        print(f"ERROR al procesar {filename}: {e}")
        return pd.DataFrame(columns=[
            '21A_Demand', '21A_Stock', '21A_SafetyStock',
            '22B_Demand', '22B_Stock', '22B_SafetyStock',
            '23C_Demand', '23C_Stock', '23C_SafetyStock'
        ])


def process_yields(filename='Yields.csv'):
    """
    Procesa el archivo Yields.csv respetando su estructura original
    """
    print(f"\nProcesando {filename}...")

    if not os.path.exists(filename):
        print(f"ADVERTENCIA: El archivo {filename} no existe en el directorio actual.")
        return pd.DataFrame()

    try:
        raw_data = pd.read_csv(filename, header=None)
        print(f"  - Forma del archivo raw: {raw_data.shape}")

        # La fila de datos comienza después de las cabeceras (típicamente fila 3)
        start_row = 2

        # Extraer filas con datos numéricos, saltando encabezados
        data_rows = raw_data.iloc[start_row:].copy()
        print(f"  - Filas de datos extraídas: {len(data_rows)}")

        # Filtrar filas que contienen solo valores numéricos
        yields_data = []
        for index, row in data_rows.iterrows():
            try:
                # Solo procesar filas con valores numéricos
                # Verificar si las columnas 1,2,3 son numéricas
                if pd.to_numeric(row[1], errors='coerce') is not None and \
                        pd.to_numeric(row[2], errors='coerce') is not None and \
                        pd.to_numeric(row[3], errors='coerce') is not None:
                    yields_row = {
                        '21A_Yield': pd.to_numeric(row[1], errors='coerce'),
                        '22B_Yield': pd.to_numeric(row[2], errors='coerce'),
                        '23C_Yield': pd.to_numeric(row[3], errors='coerce')
                    }
                    yields_data.append(yields_row)
            except Exception as e:
                print(f"  - Saltando fila {index} en {filename}: {e}")
                # No agregamos filas con error al conjunto de datos

        result_df = pd.DataFrame(yields_data)
        print(f"  - DataFrame final: {result_df.shape}")
        return result_df

    except Exception as e:
        print(f"ERROR al procesar {filename}: {e}")
        return pd.DataFrame(columns=['21A_Yield', '22B_Yield', '23C_Yield'])


def calculate_production(capacities, yields):
    """
    Calcula la producción basada en capacidades disponibles y rendimientos
    """
    print("\nCalculando producción...")

    if capacities.empty or yields.empty:
        print("  - ERROR: No hay datos suficientes para calcular producción")
        return pd.DataFrame()

    # Crear DataFrame para almacenar resultados
    production = pd.DataFrame()

    # Determinar número de periodos (el mínimo entre capacidades y yields)
    num_periods = min(len(capacities), len(yields))
    print(f"  - Número de periodos para cálculo: {num_periods}")

    # Recortar ambos DataFrames al mismo tamaño
    capacities = capacities.iloc[:num_periods].copy().reset_index(drop=True)
    yields = yields.iloc[:num_periods].copy().reset_index(drop=True)

    # Calcular producción para cada producto
    for product in ['21A', '22B', '23C']:
        try:
            production[f'{product}_Production'] = capacities[product] * yields[f'{product}_Yield']
        except Exception as e:
            print(f"  - Error al calcular producción para {product}: {e}")
            production[f'{product}_Production'] = 0.0

    print(f"  - DataFrame de producción calculado: {production.shape}")
    return production


def generate_output_format(production, supply_demand):
    """
    Genera el formato de salida requerido combinando datos de producción y demanda
    """
    print("\nGenerando formato de salida...")

    if production.empty:
        print("  - ERROR: No hay datos de producción para generar salida")
        return pd.DataFrame()

    # Determinar el número de períodos a procesar
    num_periods = len(production)
    if not supply_demand.empty:
        num_periods = min(num_periods, len(supply_demand))

    print(f"  - Generando formato para {num_periods} periodos")

    # Preparar estructura del resultado
    output_data = []

    for i in range(num_periods):
        try:
            # Calcular valores para cada periodo
            period_production = sum([
                production[f'{prod}_Production'].iloc[i]
                for prod in ['21A', '22B', '23C']
            ])

            # Para los datos de Supply_Demand, verificar si están disponibles
            if not supply_demand.empty and i < len(supply_demand):
                period_stock = sum([
                    supply_demand[f'{prod}_Stock'].iloc[i]
                    for prod in ['21A', '22B', '23C']
                ])
                period_demand = sum([
                    supply_demand[f'{prod}_Demand'].iloc[i]
                    for prod in ['21A', '22B', '23C']
                ])
                period_safety = sum([
                    supply_demand[f'{prod}_SafetyStock'].iloc[i]
                    for prod in ['21A', '22B', '23C']
                ])
            else:
                # Si no hay datos, usar NaN o 0
                period_stock = 0.0
                period_demand = 0.0
                period_safety = 0.0

            # Crear registro para este periodo
            period_data = {
                'Periodo': f'Periodo {i + 1}',
                'Produccion': period_production,
                'Stock_Final': period_stock,
                'Demanda': period_demand,
                'Stock_Seguridad': period_safety
            }
            output_data.append(period_data)

        except Exception as e:
            print(f"  - Error al generar datos para periodo {i + 1}: {e}")

    # Crear DataFrame final
    output_df = pd.DataFrame(output_data)
    print(f"  - DataFrame de salida generado: {output_df.shape}")

    return output_df


def main():
    """
    Función principal que coordina todo el proceso
    """
    print("=== INICIANDO PROCESAMIENTO DE DATOS ===")

    try:
        # Verificar que existan los archivos
        for filename in ['Boundary_Conditions.csv', 'Supply_Demand.csv', 'Yields.csv']:
            if not os.path.exists(filename):
                print(f"ADVERTENCIA: No se encuentra el archivo {filename} en el directorio actual.")
                print(f"Directorio actual: {os.getcwd()}")

        # Procesar cada archivo CSV
        capacities_df = process_boundary_conditions('Boundary_Conditions.csv')
        supply_demand_df = process_supply_demand('Supply_Demand.csv')
        yields_df = process_yields('Yields.csv')

        # Verificar si hay datos suficientes
        if capacities_df.empty or yields_df.empty:
            print("ERROR: No hay suficientes datos para continuar con el procesamiento.")
            return

        # Mostrar primeras filas para verificación
        print("\nPrimeras filas de cada DataFrame:")
        print("Capacities DataFrame:")
        print(capacities_df.head())
        print("\nSupply Demand DataFrame:")
        print(supply_demand_df.head() if not supply_demand_df.empty else "No hay datos")
        print("\nYields DataFrame:")
        print(yields_df.head())

        # Calcular producción
        production_df = calculate_production(capacities_df, yields_df)

        # Mostrar primeras filas del resultado de producción
        print("\nProduction DataFrame:")
        print(production_df.head())

        # Generar formato de salida
        output_df = generate_output_format(production_df, supply_demand_df)

        # Guardar resultado en CSV
        output_filename = 'resultado_produccion.csv'
        output_df.to_csv(output_filename, index=False)
        print(f"\nArchivo generado con éxito: {output_filename}")

        # Mostrar primeras filas del resultado final
        print("\nPrimeras filas del archivo generado:")
        print(output_df.head(10))

        print("\n=== PROCESAMIENTO COMPLETADO CON ÉXITO ===")

    except Exception as e:
        import traceback
        print(f"\nERROR CRÍTICO EN LA EJECUCIÓN: {e}")
        print(traceback.format_exc())
        print("\n=== PROCESAMIENTO TERMINADO CON ERRORES ===")


if __name__ == "__main__":
    main()