import re
import csv
import os

# --- FUNCIÓN DE NORMALIZACIÓN (sin cambios) ---
def to_inline_mode(latex_str):
    # Extraer contenido de \boxed{...}
    latex_str = re.sub(r'\\boxed\{(.+?)\}', r'\1', latex_str)
    # Quitar $$ ... $$ y $ ... $
    latex_str = re.sub(r'\$\$?(.+?)\$\$?', r'\1', latex_str)
    # Envolver en $ ... $
    return f"${latex_str.strip()}$"

# --- CONFIGURACIÓN DEL EXTRACTOR (sin cambios) ---
palabras_clave = [
    "Respuesta Final", "Respuesta", "Por lo tanto", "Conclusión",
    "Resultado final", "Es decir", "La solución de la ecuación es",
    "El resultado de la división es", "el valor del ángulo es"
]
palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

# Regex separadas por prioridad
regex_boxed = r'\\boxed\{.*?\}'  # Prioridad 1
regex_latex_otros = r'\$\$.*?\$\$|\$[^$]*\$'
regex_numeros = r'\*{2}\s*-?(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?\s*\*{2}|-?\b(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?\b'

# --- FUNCIÓN DE EXTRACCIÓN (con un pequeño ajuste en los prints) ---
def extraer_respuesta(texto, numero_fila):
    """
    Extrae la respuesta de un texto dado, siguiendo una lógica de prioridades.
    """
    print(f"--- Procesando Fila {numero_fila} ---")

    # Si el texto de entrada está vacío o es solo espacio en blanco, no hacer nada.
    if not texto or texto.isspace():
        print("Celda vacía. Saltando...")
        return None

    match_keyword = re.search(patron_keywords, texto, re.IGNORECASE)
    if not match_keyword:
        print("No se encontró palabra clave.")
        return None

    keyword_encontrada = match_keyword.group(0)
    texto_relevante = texto[match_keyword.end():]

    # --- LÓGICA DE PRIORIDAD SECUENCIAL ---
    # Prioridad 1: Buscar \boxed{...}
    boxed_matches = re.findall(regex_boxed, texto_relevante, re.DOTALL)
    if boxed_matches:
        respuesta_final = to_inline_mode(boxed_matches[-1])  # Aplicar normalización
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado encontrado (Prioridad 1: Boxed):")
        return respuesta_final

    # Si no hay \boxed, buscar otros tipos de respuesta
    regex_otros = f"({regex_latex_otros})|({regex_numeros})"
    otros_matches = re.findall(regex_otros, texto_relevante, re.DOTALL)

    if not otros_matches:
        print(f"Palabra clave: '{keyword_encontrada}'. No se encontró resultado válido después.")
        return None

    # Tomar el último resultado encontrado (sea LaTeX o numérico)
    ultimo_match_tupla = otros_matches[-1]
    ultimo_match_str = next(filter(bool, ultimo_match_tupla), "").strip()

    # Prioridad 2: ¿Es LaTeX (no-boxed)?
    if re.fullmatch(regex_latex_otros, ultimo_match_str):
        respuesta_final = to_inline_mode(ultimo_match_str)  # Aplicar normalización
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado encontrado (Prioridad 2: LaTeX):")
        return respuesta_final

    # Prioridad 3: Es numérico
    else:
        respuesta_final = ultimo_match_str.strip('°* ')
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado encontrado (Prioridad 3: Numérico):")
        return respuesta_final

# --- NUEVA FUNCIÓN PARA PROCESAR EL CSV ---
def procesar_csv(archivo_entrada, archivo_salida):
    """
    Lee un archivo CSV, procesa la primera columna de cada fila
    y escribe los resultados en un nuevo archivo CSV.
    """
    print(f"Leyendo datos desde '{archivo_entrada}'...")
    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as infile, \
             open(archivo_salida, mode='w', encoding='utf-8', newline='') as outfile:

            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)

            # Escribir la cabecera en el archivo de salida
            # Intentamos leer la cabecera del original si existe
            try:
                cabecera_original = next(csv_reader)
                csv_writer.writerow(cabecera_original + ['Respuesta Extraída'])
                fila_inicial = 2 # Empezamos a contar desde la fila 2 porque la 1 es cabecera
            except StopIteration:
                cabecera_original = ['Texto Original'] # Si no hay cabecera, la creamos
                csv_writer.writerow(cabecera_original + ['Respuesta Extraída'])
                # Rebobinamos el archivo para leer desde el principio
                infile.seek(0)
                fila_inicial = 1


            # Procesar cada fila del archivo de entrada
            for i, fila in enumerate(csv_reader, start=fila_inicial):
                if not fila:  # Ignorar filas completamente vacías
                    continue

                texto_a_procesar = fila[0]
                resultado = extraer_respuesta(texto_a_procesar, numero_fila=i)

                # Escribir la fila original más el resultado en el archivo de salida
                csv_writer.writerow(fila + [resultado if resultado is not None else ""])

        print(f"\n¡Proceso completado! Resultados guardados en '{archivo_salida}'")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
        print("Por favor, asegúrate de que el archivo existe en la misma carpeta que el script y se llama correctamente.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    # Define los nombres de tus archivos de entrada y salida
    archivo_csv_entrada = "datos.csv"
    archivo_csv_salida = "resultados.csv"
    
    # Llama a la función principal para iniciar el procesamiento
    procesar_csv(archivo_csv_entrada, archivo_csv_salida)