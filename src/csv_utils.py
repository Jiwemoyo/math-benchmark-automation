
import csv
from .extractor import extraer_respuesta


def procesar_csv(archivo_entrada, archivo_salida, idx_id, idx_respuesta, idx_ia):
    print(f"Leyendo datos desde '{archivo_entrada}'...")
    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as infile, \
             open(archivo_salida, mode='w', encoding='utf-8', newline='') as outfile:
            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            try:
                header_original = next(csv_reader)
                min_cols = max(idx_id, idx_respuesta, idx_ia) + 1
                if len(header_original) < min_cols:
                    print(f"Error: El archivo de entrada no tiene suficientes columnas en el encabezado (necesita al menos {min_cols}).")
                    return
                header_salida = [
                    header_original[idx_id],
                    header_original[idx_respuesta],
                    header_original[idx_ia],
                    "respuesta extraida"
                ]
                csv_writer.writerow(header_salida)
            except StopIteration:
                print("Error: El archivo de entrada está vacío.")
                return
            for i, fila in enumerate(csv_reader, start=2):
                if not fila:
                    continue
                if len(fila) < min_cols:
                    print(f"--- Omitiendo Fila {i}: tiene menos de {min_cols} columnas ---")
                    continue
                col_id = fila[idx_id]
                col_respuesta = fila[idx_respuesta]
                col_ia = fila[idx_ia]
                resultado = extraer_respuesta(col_ia, numero_fila=i)
                fila_salida = [col_id, col_respuesta, col_ia, resultado if resultado is not None else ""]
                csv_writer.writerow(fila_salida)
        print(f"\n¡Proceso completado! Resultados guardados en '{archivo_salida}'")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
