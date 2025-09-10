import re
import csv
import os

# --- FUNCIÓN DE NORMALIZACIÓN (sin cambios) ---
def to_inline_mode(latex_str):
    content = latex_str
    boxed_match = re.search(r'\\boxed\{(.*)\}', content, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
    content = re.sub(r'^\$\$?|\$\$?$', '', content).strip()
    return f"${content}$"

# --- CONFIGURACIÓN DEL EXTRACTOR (sin cambios) ---
palabras_clave = [
    "Respuesta Final", "Respuesta", "Por lo tanto", "Conclusión", 
    "Resultado final", "Es decir", "La solución de la ecuación es",
    "El resultado de la división es", "el valor del ángulo es"
]
palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)
patron_secundario = r'\b(es|son|vale|mide|sea|es el|es la)\b\s*:?'
regex_boxed = r'\\boxed\{(?:[^{}]|{[^{}]*})*\}' 
regex_latex_otros = r'\$\$.*?\$\$|\$[^$]*\$'
regex_numeros = r'''
    \b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|
    \b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|
    \*\*[^*]+\*\*|
    \*[^*]+\*|
    \b\d+/\d+\b|
    \b\d+\s*/\s*\d+\b|
    -?\d+(?:\.\d+)?\°?|
    \b\d+\b
'''

# --- FUNCIÓN DE EXTRACCIÓN (sin cambios) ---
def extraer_respuesta(texto, numero_fila):
    if not texto or texto.isspace():
        print(f"--- Procesando Fila {numero_fila}: Columna G vacía ---")
        return None
        
    print(f"--- Procesando Fila {numero_fila} ---")

    todas_keywords = list(re.finditer(patron_keywords, texto, re.IGNORECASE))
    if not todas_keywords:
        print("No se encontró palabra clave principal.")
        return None
    
    match_keyword = todas_keywords[-1]
    keyword_encontrada = match_keyword.group(0)
    print(f"Palabra clave encontrada (última): '{keyword_encontrada}'")
    
    texto_despues_keyword_principal = texto[match_keyword.end():]
    
    match_secundario = re.search(patron_secundario, texto_despues_keyword_principal, re.IGNORECASE)
    if match_secundario:
        print(f"Palabra secundaria encontrada: '{match_secundario.group(0)}'. Acotando búsqueda.")
        texto_relevante = texto_despues_keyword_principal[match_secundario.end():]
    else:
        texto_relevante = texto_despues_keyword_principal

    candidatos = []
    
    boxed_match = re.search(regex_boxed, texto_relevante, re.DOTALL)
    if boxed_match:
        candidatos.append({'tipo': 'boxed', 'pos': boxed_match.start(), 'valor': boxed_match.group(0)})

    latex_match = re.search(regex_latex_otros, texto_relevante, re.DOTALL)
    if latex_match:
        candidatos.append({'tipo': 'latex', 'pos': latex_match.start(), 'valor': latex_match.group(0)})

    numero_match = re.search(regex_numeros, texto_relevante, re.VERBOSE)
    if numero_match:
        candidatos.append({'tipo': 'numero', 'pos': numero_match.start(), 'valor': numero_match.group(0)})

    if not candidatos:
        print(f"Palabra clave: '{keyword_encontrada}'. No se encontró resultado válido.")
        return None

    mejor_candidato = sorted(candidatos, key=lambda x: x['pos'])[0]
    
    if mejor_candidato['tipo'] == 'boxed':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
    elif mejor_candidato['tipo'] == 'latex':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
    else:
        respuesta_final = re.sub(r'^\*+|\*+$', '', mejor_candidato['valor']).strip()
    
    print(f"Resultado: {respuesta_final}")
    return respuesta_final

# --- FUNCIÓN PARA PROCESAR EL CSV (MODIFICADA) ---
def procesar_csv(archivo_entrada, archivo_salida):
    """
    Lee un CSV con encabezados, extrae las columnas A, E y G, aplica el script 
    a la columna G y escribe un nuevo CSV con un encabezado que incluye 'respuesta extraida'.
    """
    print(f"Leyendo datos desde '{archivo_entrada}'...")
    try:
        with open(archivo_entrada, mode='r', encoding='utf-8') as infile, \
             open(archivo_salida, mode='w', encoding='utf-8', newline='') as outfile:

            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)

            # --- MANEJO DE ENCABEZADOS ---
            try:
                # 1. Leer la primera fila como el encabezado original
                header_original = next(csv_reader)
                
                # 2. Comprobar que el encabezado tenga suficientes columnas
                if len(header_original) < 7:
                    print(f"Error: El archivo de entrada no tiene suficientes columnas en el encabezado (necesita al menos 7).")
                    return

                # 3. Construir el nuevo encabezado de salida
                header_salida = [
                    header_original[0],          # Encabezado de la columna A
                    header_original[4],          # Encabezado de la columna E
                    header_original[6],          # Encabezado de la columna G
                    "respuesta extraida"         # Nuevo encabezado
                ]
                
                # 4. Escribir la nueva fila de encabezado en el archivo de salida
                csv_writer.writerow(header_salida)

            except StopIteration:
                print("Error: El archivo de entrada está vacío.")
                return # Salir si no hay filas para leer

            # --- PROCESAMIENTO DE DATOS ---
            # Procesar el resto de las filas (empezando el conteo desde la fila 2)
            for i, fila in enumerate(csv_reader, start=2):
                if not fila:
                    continue

                if len(fila) < 7:
                    print(f"--- Omitiendo Fila {i}: tiene menos de 7 columnas ---")
                    continue
                
                col_A = fila[0]
                col_E = fila[4]
                col_G = fila[6]
                
                resultado = extraer_respuesta(col_G, numero_fila=i)
                
                fila_salida = [col_A, col_E, col_G, resultado if resultado is not None else ""]
                
                csv_writer.writerow(fila_salida)

        print(f"\n¡Proceso completado! Resultados guardados en '{archivo_salida}'")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- BLOQUE DE EJECUCIÓN PRINCIPAL (sin cambios) ---
if __name__ == "__main__":
    archivo_csv_entrada = "datos.csv"
    archivo_csv_salida = "resultados.csv"
    
    procesar_csv(archivo_csv_entrada, archivo_csv_salida)