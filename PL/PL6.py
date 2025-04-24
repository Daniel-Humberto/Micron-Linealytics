from pulp import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def cargar_datos_csv(ruta_archivo, corregir_problemas=True):
    """
    Carga los datos desde un archivo CSV con manejo mejorado de errores y diagnóstico.
    Retorna un diccionario con los datos procesados.
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")

        # Cargar el archivo CSV
        print(f"Intentando cargar el archivo: {ruta_archivo}")
        df = pd.read_csv(ruta_archivo)

        # Mostrar estructura del dataframe para diagnóstico
        print("\nEstructura del archivo CSV:")
        print(f"Columnas encontradas: {list(df.columns)}")
        print(f"Número de filas: {len(df)}")
        print("\nPrimeras 5 filas del archivo:")
        print(df.head())

        # Detectar y corregir problemas comunes en el formato
        if corregir_problemas:
            # 1. Limpiar nombres de columnas (eliminar espacios, etc.)
            df.columns = [col.strip() for col in df.columns]

            # 2. Reemplazar valores no numéricos
            df = df.replace('', np.nan)
            for col in df.columns:
                if col != 'Periodo':  # No convertir la columna de periodo
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        print(f"Advertencia: No se pudo convertir la columna {col} a números.")

        # Extraer los datos relevantes
        periodos = df['Periodo'].tolist()

        # Manejo de demandas
        if 'Demanda' in df.columns:
            demandas = df['Demanda'].fillna(0).tolist()
        else:
            print("Advertencia: No se encontró la columna 'Demanda'. Se usará 0 para todos los períodos.")
            demandas = [0] * len(periodos)

        # Manejo de stocks de seguridad
        if 'Stock_Seguridad' in df.columns:
            stocks_seguridad = df['Stock_Seguridad'].fillna(0).tolist()
        else:
            print("Advertencia: No se encontró la columna 'Stock_Seguridad'. Se usará 0 para todos los períodos.")
            stocks_seguridad = [0] * len(periodos)

        # Diagnóstico de valores extremos
        print("\nDiagnóstico de valores:")
        print(f"Demanda mínima: {min(demandas)}, máxima: {max(demandas)}")
        print(f"Stock de seguridad mínimo: {min(stocks_seguridad)}, máximo: {max(stocks_seguridad)}")

        # Stock inicial
        stock_inicial = 0
        if 'Stock_Final' in df.columns and not df['Stock_Final'].isna().all():
            # Buscar un buen valor para el stock inicial
            ultimos_stocks = df['Stock_Final'].dropna().tolist()
            if ultimos_stocks:
                stock_inicial = ultimos_stocks[-1]
                print(f"Stock inicial detectado: {stock_inicial}")

                # Si el stock inicial es negativo o muy grande, ofrecer alternativas
                if stock_inicial < 0:
                    print("ADVERTENCIA: El stock inicial es negativo, lo cual no es físicamente posible.")
                    print("Se reemplazará con un valor de 0.")
                    stock_inicial = 0
                elif abs(stock_inicial) > 1e9:
                    print("ADVERTENCIA: El stock inicial tiene un valor extremo.")
                    print(f"Valor original: {stock_inicial}")
                    print("Se reemplazará con un valor más razonable: 1000")
                    stock_inicial = 1000

        # Limitar el número de períodos si es excesivo
        max_periodos = 52  # Un año de semanas
        if len(periodos) > max_periodos:
            print(f"\nADVERTENCIA: El número de períodos ({len(periodos)}) es muy alto.")
            print(f"Para facilitar la optimización, se limitará a los primeros {max_periodos} períodos.")
            periodos = periodos[:max_periodos]
            demandas = demandas[:max_periodos]
            stocks_seguridad = stocks_seguridad[:max_periodos]

        # Verificar valores negativos o extremos en demandas y stocks de seguridad
        for i in range(len(demandas)):
            if demandas[i] < 0:
                print(f"Corrigiendo demanda negativa en período {periodos[i]}: {demandas[i]} → 0")
                demandas[i] = 0
            elif demandas[i] > 1e6:
                print(f"Corrigiendo demanda extrema en período {periodos[i]}: {demandas[i]} → 1000")
                demandas[i] = 1000

            if stocks_seguridad[i] < 0:
                print(f"Corrigiendo stock de seguridad negativo en período {periodos[i]}: {stocks_seguridad[i]} → 0")
                stocks_seguridad[i] = 0
            elif stocks_seguridad[i] > 1e6:
                print(f"Corrigiendo stock de seguridad extremo en período {periodos[i]}: {stocks_seguridad[i]} → 100")
                stocks_seguridad[i] = 100

        return {
            'periodos': periodos,
            'demandas': demandas,
            'stocks_seguridad': stocks_seguridad,
            'stock_inicial': stock_inicial,
            'num_periodos': len(periodos)
        }

    except Exception as e:
        print(f"Error al cargar los datos del CSV: {str(e)}")
        print("\nVerificando si el archivo tiene un formato diferente...")

        try:
            # Intentar cargar con un enfoque más robusto
            df = pd.read_csv(ruta_archivo, sep=None, engine='python')
            print("Se detectó un formato alternativo. Intentando procesar...")
            print(df.head())

            # Intentar detectar columnas clave
            columnas = list(df.columns)
            print(f"Columnas detectadas: {columnas}")

            # Crear un conjunto mínimo de datos para continuar
            num_filas = len(df)
            periodos = [f"Semana {i + 1}" for i in range(num_filas)]
            demandas = [100] * num_filas  # Valores de ejemplo
            stocks_seguridad = [20] * num_filas  # Valores de ejemplo

            print("Se han generado datos de ejemplo para continuar.")
            print("IMPORTANTE: Estos NO son sus datos reales. Por favor corrija el formato del CSV.")

            return {
                'periodos': periodos,
                'demandas': demandas,
                'stocks_seguridad': stocks_seguridad,
                'stock_inicial': 100,
                'num_periodos': num_filas
            }

        except:
            print("\nNo se pudo recuperar de los errores en el archivo CSV.")
            print("Creando un conjunto mínimo de datos para demostración:")

            # Crear un conjunto mínimo de ejemplo
            periodos = [f"Semana {i + 1}" for i in range(5)]
            demandas = [100, 120, 140, 110, 130]
            stocks_seguridad = [20, 20, 20, 20, 0]

            print("Se han generado datos de ejemplo para demostración.")
            print("IMPORTANTE: Estos NO son sus datos reales.")

            return {
                'periodos': periodos,
                'demandas': demandas,
                'stocks_seguridad': stocks_seguridad,
                'stock_inicial': 50,
                'num_periodos': 5
            }


def optimize_production(
        initial_stock,
        demands,
        yield_percentage,
        density,
        max_productivity,
        safety_stocks=None,
        objective="min",  # "min" to minimize productivity or "max" to maximize
        debug=False
):
    num_periods = len(demands)

    if safety_stocks is None:
        safety_stocks = [0] * num_periods
    elif len(safety_stocks) != num_periods:
        raise ValueError("La longitud de stocks_seguridad debe ser igual al número de períodos.")

    if debug:
        print("\nConfiguración del modelo de optimización:")
        print(f"Stock inicial: {initial_stock}")
        print(f"Rendimiento: {yield_percentage}")
        print(f"Densidad: {density}")
        print(f"Productividad máxima: {max_productivity}")
        print(f"Objetivo: {'Minimizar' if objective == 'min' else 'Maximizar'} producción")
        print("\nResumen de restricciones:")
        print(f"Factor de producción efectiva: {yield_percentage * density}")

    # 1. Crear problema
    direction = LpMinimize if objective == "min" else LpMaximize
    prob = LpProblem("Optimizacion_Produccion", direction)

    # 2. Variables de decisión
    production_vars = [LpVariable(f"P_{t}", 0, max_productivity) for t in range(num_periods)]

    # 3. Función objetivo
    prob += lpSum(production_vars), "Produccion_Total"

    # 4. Restricciones
    stock = initial_stock
    stock_vars = []  # Para seguimiento de niveles de stock finales

    for t in range(num_periods):
        # Cálculo del balance de inventario
        new_stock = stock + (production_vars[t] * yield_percentage * density) - demands[t]
        prob += new_stock >= safety_stocks[t], f"Stock_Seguridad_{t}"
        stock_vars.append(new_stock)
        stock = new_stock  # Llevar el stock hacia adelante

    # El stock final debe ser igual o mayor que el último stock de seguridad
    prob += stock >= safety_stocks[-1], "Stock_Final_Minimo"

    # 5. Resolver
    status = prob.solve(PULP_CBC_CMD(msg=debug))

    # 6. Extraer resultados
    if LpStatus[prob.status] == 'Optimal':
        optimal_value = value(prob.objective)
        production_levels = [value(var) for var in production_vars]
        ending_stocks = [value(s) for s in stock_vars]

        return {
            'optimal_value': optimal_value,
            'production_levels': production_levels,
            'ending_stocks': ending_stocks,
            'status': LpStatus[prob.status]
        }
    else:
        if debug:
            print("\nNo se encontró solución óptima. Diagnóstico del problema:")
            print(f"Estado: {LpStatus[prob.status]}")

            # Analizar por qué podría ser inviable
            if LpStatus[prob.status] == 'Infeasible':
                total_demand = sum(demands)
                max_possible_production = max_productivity * num_periods * yield_percentage * density

                print(f"Demanda total: {total_demand}")
                print(f"Producción máxima posible: {max_possible_production}")

                if total_demand > max_possible_production + initial_stock:
                    print("DIAGNÓSTICO: La demanda total excede la capacidad máxima de producción.")
                    print("Recomendación: Aumentar la productividad máxima o reducir la demanda.")

                # Verificar balance inicial
                if initial_stock < safety_stocks[0]:
                    print(
                        "DIAGNÓSTICO: El stock inicial es menor que el stock de seguridad requerido para el primer período.")
                    print(f"Stock inicial: {initial_stock}, Stock de seguridad requerido: {safety_stocks[0]}")

        return {
            'status': LpStatus[prob.status]
        }


def plot_results(periodos, production, stocks, demands, safety_stocks):
    """
    Genera gráficas para visualizar los resultados de la optimización.
    """
    plt.figure(figsize=(12, 8))

    # Convertir nombres de periodos a etiquetas
    etiquetas_periodos = [str(p) for p in periodos]
    indices = list(range(len(etiquetas_periodos)))

    plt.plot(indices, production, marker='o', linewidth=2, label="Producción")
    plt.plot(indices, demands, marker='s', linestyle='--', linewidth=2, label="Demanda")
    plt.plot(indices, stocks, marker='^', linestyle=':', linewidth=2, label="Stock Final")
    plt.plot(indices, safety_stocks, marker='x', linestyle='-.', linewidth=2, label="Stock Seguridad")

    plt.title("Optimización de Producción Semanal", fontsize=16)
    plt.xlabel("Periodo (Semana)", fontsize=14)
    plt.ylabel("Unidades", fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=12)

    # Manejar etiquetas para evitar sobrecarga
    if len(indices) > 20:
        # Mostrar solo algunas etiquetas para evitar congestión
        mostrar_indices = np.linspace(0, len(indices) - 1, 10, dtype=int)
        plt.xticks(mostrar_indices, [etiquetas_periodos[i] for i in mostrar_indices], rotation=45)
    else:
        plt.xticks(indices, etiquetas_periodos, rotation=45)

    plt.tight_layout()

    # Guardar la gráfica
    plt.savefig('resultado_optimizacion.png')
    print("Gráfica guardada como 'resultado_optimizacion.png'")

    # Mostrar la gráfica
    plt.show()


def guardar_resultados_csv(datos_entrada, resultados, ruta_salida='resultado_optimizacion_nuevo.csv'):
    """
    Guarda los resultados de la optimización en un archivo CSV.
    """
    try:
        df_resultados = pd.DataFrame({
            'Periodo': datos_entrada['periodos'],
            'Produccion': resultados['production_levels'],
            'Stock_Final': resultados['ending_stocks'],
            'Demanda': datos_entrada['demandas'],
            'Stock_Seguridad': datos_entrada['stocks_seguridad']
        })

        df_resultados.to_csv(ruta_salida, index=False)
        print(f"Resultados guardados exitosamente en '{ruta_salida}'")
        return True
    except Exception as e:
        print(f"Error al guardar los resultados: {e}")
        return False


def validar_solucion(resultados, datos):
    """
    Valida la solución para asegurar que es viable y cumple todas las restricciones.
    """
    if resultados['status'] != 'Optimal':
        return False, "No se encontró una solución óptima."

    # Validar que la producción no excede el máximo
    for i, prod in enumerate(resultados['production_levels']):
        if prod > MAX_PRODUCTIVITY:
            return False, f"La producción en el período {i + 1} excede la capacidad máxima."

    # Validar que los stocks finales cumplen con los stocks de seguridad
    for i, (stock, safety) in enumerate(zip(resultados['ending_stocks'], datos['stocks_seguridad'])):
        if stock < safety - 0.001:  # Pequeña tolerancia para errores de punto flotante
            return False, f"El stock final en el período {i + 1} no cumple con el stock de seguridad requerido."

    return True, "La solución es viable y cumple todas las restricciones."


def intentar_resolver_con_parametros_alternativos(datos, intento=1, max_intentos=5):
    """
    Intenta encontrar una solución usando diferentes configuraciones de parámetros.
    """
    print(f"\nIntentando resolución alternativa (intento {intento}/{max_intentos})...")

    # Parámetros originales
    yield_percentage_original = YIELD_PERCENTAGE
    density_original = DENSITY
    max_productivity_original = MAX_PRODUCTIVITY
    stock_inicial_original = datos['stock_inicial']

    # Estrategias de ajuste según el intento
    if intento == 1:
        # Aumentar la productividad máxima
        MAX_PRODUCTIVITY_NUEVO = MAX_PRODUCTIVITY * 5
        print(f"Aumentando productividad máxima: {MAX_PRODUCTIVITY} → {MAX_PRODUCTIVITY_NUEVO}")

        resultado = optimize_production(
            datos['stock_inicial'],
            datos['demandas'],
            YIELD_PERCENTAGE,
            DENSITY,
            MAX_PRODUCTIVITY_NUEVO,
            datos['stocks_seguridad'],
            objective=OBJETIVO,
            debug=True
        )

    elif intento == 2:
        # Aumentar el rendimiento y la densidad
        YIELD_PERCENTAGE_NUEVO = min(1.0, YIELD_PERCENTAGE * 1.5)
        DENSITY_NUEVO = min(1.0, DENSITY * 1.5)
        print(f"Aumentando rendimiento: {YIELD_PERCENTAGE} → {YIELD_PERCENTAGE_NUEVO}")
        print(f"Aumentando densidad: {DENSITY} → {DENSITY_NUEVO}")

        resultado = optimize_production(
            datos['stock_inicial'],
            datos['demandas'],
            YIELD_PERCENTAGE_NUEVO,
            DENSITY_NUEVO,
            MAX_PRODUCTIVITY * 2,
            datos['stocks_seguridad'],
            objective=OBJETIVO,
            debug=True
        )

    elif intento == 3:
        # Reducir stocks de seguridad
        stocks_seguridad_nuevos = [max(0, s * 0.5) for s in datos['stocks_seguridad']]
        print("Reduciendo stocks de seguridad al 50% de los valores originales")

        resultado = optimize_production(
            datos['stock_inicial'],
            datos['demandas'],
            YIELD_PERCENTAGE,
            DENSITY,
            MAX_PRODUCTIVITY * 3,
            stocks_seguridad_nuevos,
            objective=OBJETIVO,
            debug=True
        )

    elif intento == 4:
        # Ajustar stock inicial
        stock_inicial_nuevo = max(sum(datos['stocks_seguridad'][:3]), 1000)
        print(f"Ajustando stock inicial: {datos['stock_inicial']} → {stock_inicial_nuevo}")

        resultado = optimize_production(
            stock_inicial_nuevo,
            datos['demandas'],
            YIELD_PERCENTAGE,
            DENSITY,
            MAX_PRODUCTIVITY * 4,
            datos['stocks_seguridad'],
            objective=OBJETIVO,
            debug=True
        )

    elif intento == 5:
        # Usar configuración extrema
        print("Usando configuración máxima para encontrar cualquier solución viable")
        stock_inicial_nuevo = max(sum(datos['demandas'][:3]), 5000)
        stocks_seguridad_nuevos = [0] * len(datos['stocks_seguridad'])

        resultado = optimize_production(
            stock_inicial_nuevo,
            datos['demandas'],
            1.0,  # Rendimiento máximo
            1.0,  # Densidad máxima
            100000,  # Productividad muy alta
            stocks_seguridad_nuevos,
            objective=OBJETIVO,
            debug=True
        )

    if resultado['status'] == 'Optimal':
        print("\n✅ Se encontró una solución viable con parámetros alternativos!")
        return resultado, intento
    elif intento < max_intentos:
        return intentar_resolver_con_parametros_alternativos(datos, intento + 1, max_intentos)
    else:
        print("\n❌ No se pudo encontrar una solución después de varios intentos.")
        return {'status': 'Infeasible'}, 0


if __name__ == "__main__":
    # Parámetros fijos del sistema
    YIELD_PERCENTAGE = 0.8  # Rendimiento del proceso
    DENSITY = 0.9  # Densidad
    MAX_PRODUCTIVITY = 300  # Productividad máxima por período
    OBJETIVO = "min"  # "min" para minimizar producción, "max" para maximizar

    # Archivo CSV de entrada
    ARCHIVO_CSV = "resultado_produccion.csv"

    print("Sistema de Optimización de Producción Semanal")
    print("=============================================")

    try:
        # Cargar datos del CSV con corrección de problemas
        print(f"Cargando datos desde '{ARCHIVO_CSV}'...")
        datos = cargar_datos_csv(ARCHIVO_CSV)

        print(f"\nSe han cargado datos para {datos['num_periodos']} períodos.")
        print(f"Stock Inicial: {datos['stock_inicial']}")

        # Ejecutar optimización
        print("\nEjecutando optimización de producción...")
        resultado = optimize_production(
            datos['stock_inicial'],
            datos['demandas'],
            YIELD_PERCENTAGE,
            DENSITY,
            MAX_PRODUCTIVITY,
            datos['stocks_seguridad'],
            objective=OBJETIVO,
            debug=True
        )

        print(f"\nEstado de la Optimización: {resultado['status']}")

        # Si no se encuentra solución, intentar con parámetros alternativos
        if resultado['status'] != 'Optimal':
            print("\nBuscando soluciones alternativas...")
            resultado_alternativo, intento_exitoso = intentar_resolver_con_parametros_alternativos(datos)

            if resultado_alternativo['status'] == 'Optimal':
                resultado = resultado_alternativo
                print(f"\nSe encontró una solución viable en el intento {intento_exitoso}.")

        if resultado['status'] == 'Optimal':
            # Validar la solución
            es_viable, mensaje = validar_solucion(resultado, datos)

            if es_viable:
                print(f"✅ {mensaje}")
                print(f"Valor Óptimo ({'mínimo' if OBJETIVO == 'min' else 'máximo'}): {resultado['optimal_value']:.2f}")

                # Mostrar resultados resumidos
                num_mostrar = min(10, datos['num_periodos'])
                print(f"\nResultados (mostrando primeros {num_mostrar} períodos):")
                print("=" * 80)
                print(f"{'Periodo':<15} {'Producción':<15} {'Demanda':<15} {'Stock Final':<15} {'Stock Seguridad':<15}")
                print("-" * 80)

                for i in range(num_mostrar):
                    print(f"{datos['periodos'][i]:<15} {resultado['production_levels'][i]:<15.2f} "
                          f"{datos['demandas'][i]:<15.2f} {resultado['ending_stocks'][i]:<15.2f} "
                          f"{datos['stocks_seguridad'][i]:<15.2f}")

                if datos['num_periodos'] > num_mostrar:
                    print("...")

                # Guardar resultados
                guardar_resultados_csv(datos, resultado)

                # Mostrar gráficas
                plot_results(
                    datos['periodos'],
                    resultado['production_levels'],
                    resultado['ending_stocks'],
                    datos['demandas'],
                    datos['stocks_seguridad']
                )
            else:
                print(f"⚠️ Advertencia: {mensaje}")
                print("Se recomienda revisar los parámetros y restricciones.")
        else:
            print("\n❌ No se pudo encontrar una solución viable con los parámetros actuales.")
            print("\nAnálisis del problema:")
            print("1. Revise el formato del archivo CSV y asegúrese de que los datos son correctos.")
            print("2. El stock inicial extremadamente negativo sugiere un problema con los datos.")
            print("3. Verifique que las demandas sean valores razonables para su contexto.")
            print("4. Considere reducir el número de períodos si es excesivamente alto.")

            print("\nAcciones recomendadas:")
            print("1. Corregir el archivo CSV asegurando que:")
            print(
                "   - Las columnas tengan los nombres correctos: Periodo, Produccion, Stock_Final, Demanda, Stock_Seguridad")
            print("   - Los valores numéricos sean razonables (no negativos para stock y demanda)")
            print("   - El stock inicial sea un valor físicamente posible (no negativo)")
            print("2. Ejecutar el programa nuevamente con los datos corregidos.")

    except Exception as e:
        print(f"\n❌ Error en la ejecución: {str(e)}")
        import traceback

        traceback.print_exc()
        print("\nPor favor, verifique:")
        print("1. Que el archivo CSV existe y tiene el formato correcto.")
        print("2. Que los datos son numéricos y válidos.")
        print("3. Que todas las columnas requeridas están presentes.")