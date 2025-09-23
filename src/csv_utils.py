
import csv
from .extractor import extraer_respuesta

# Índices de columnas configurables (0 = A, 1 = B, ...)
COLUMNA_A_IDX = 0  # Columna A
COLUMNA_E_IDX = 4  # Columna E
COLUMNA_G_IDX = 5  # Columna G (la que se procesa con IA)

def procesar_csv(archivo_entrada, archivo_salida):
    print(f"Leyendo datos desde '{archivo_entrada}'...")
    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as infile, \
             open(archivo_salida, mode='w', encoding='utf-8', newline='') as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            try:
                header_original = next(csv_reader)
                if len(header_original) < 7:
                    print(f"Error: El archivo de entrada no tiene suficientes columnas en el encabezado (necesita al menos 7).")
                    return
                header_salida = [
                    header_original[COLUMNA_A_IDX],
                    header_original[COLUMNA_E_IDX],
                    header_original[COLUMNA_G_IDX],
                    "respuesta extraida"
                ]
                csv_writer.writerow(header_salida)
            except StopIteration:
                print("Error: El archivo de entrada está vacío.")
                return
            for i, fila in enumerate(csv_reader, start=2):
                if not fila:
                    continue
                if len(fila) < 7:
                    print(f"--- Omitiendo Fila {i}: tiene menos de 7 columnas ---")
                    continue
                col_A = fila[COLUMNA_A_IDX]
                col_E = fila[COLUMNA_E_IDX]
                col_G = fila[COLUMNA_G_IDX]
                resultado = extraer_respuesta(col_G, numero_fila=i)
                fila_salida = [col_A, col_E, col_G, resultado if resultado is not None else ""]
                csv_writer.writerow(fila_salida)
        print(f"\n¡Proceso completado! Resultados guardados en '{archivo_salida}'")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
