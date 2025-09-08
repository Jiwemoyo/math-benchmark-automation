import re
import csv
import os

# --- FUNCIÓN DE NORMALIZACIÓN (Tu versión mejorada) ---
def to_inline_mode(latex_str):
    content = latex_str
    # Usar regex para extraer contenido de \boxed de forma segura
    boxed_match = re.search(r'\\boxed\{(.*)\}', content, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
    
    # Quitar delimitadores $$ o $ de los bordes
    content = re.sub(r'^\$\$?|\$\$?$', '', content).strip()
    return f"${content}$"

# --- CONFIGURACIÓN DEL EXTRACTOR (Tu versión mejorada) ---
palabras_clave = [
    "Respuesta Final", "Respuesta", "Por lo tanto", "Conclusión", 
    "Resultado final", "Es decir", "La solución de la ecuación es",
    "El resultado de la división es", "el valor del ángulo es"
]
palabras_clave.sort(key=len, reverse=True)
# Corregí un pequeño typo aquí ("is" por "es")
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

patron_secundario = r'\b(es|son|vale|mide|sea|es el|es la)\b\s*:?'

# Regex de formatos de respuesta (Tu versión mejorada)
regex_boxed = r'\\boxed\{(?:[^{}]|{[^{}]*})*\}' 
regex_latex_otros = r'\$\$.*?\$\$|\$[^$]*\$'
regex_numeros = r'''
    # Números con comas (508,536)
    \b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|
    # Números con puntos (508.536)  
    \b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|
    # Números en negrita doble (**2**, **508,536**)
    \*\*[^*]+\*\*|
    # Números en negrita simple (*2*, *508,536*)
    \*[^*]+\*|
    # Fracciones (3/4, 1/2, etc.)
    \b\d+/\d+\b|
    # Fracciones con espacios opcionales (3 / 4, 1 / 2, etc.)
    \b\d+\s*/\s*\d+\b|
    # Números decimales simples con ° opcional
    -?\d+(?:\.\d+)?\°?|
    # Números enteros simples
    \b\d+\b
'''

# --- FUNCIÓN DE EXTRACCIÓN (Tu lógica avanzada, con ajuste para logging) ---
def extraer_respuesta(texto, numero_fila):
    if not texto or texto.isspace():
        print(f"--- Procesando Fila {numero_fila}: Vacía ---")
        return None
        
    print(f"--- Procesando Fila {numero_fila} ---")

    # Buscar TODAS las ocurrencias y tomar la ÚLTIMA
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

    # --- Lógica "El Más Cercano Gana" ---
    candidatos = []
    
    boxed_match = re.search(regex_boxed, texto_relevante, re.DOTALL)
    if boxed_match:
        candidatos.append({'tipo': 'boxed', 'pos': boxed_match.start(), 'valor': boxed_match.group(0)})
        print(f"Candidato boxed encontrado: {boxed_match.group(0)}")

    latex_match = re.search(regex_latex_otros, texto_relevante, re.DOTALL)
    if latex_match:
        candidatos.append({'tipo': 'latex', 'pos': latex_match.start(), 'valor': latex_match.group(0)})
        print(f"Candidato latex encontrado: {latex_match.group(0)}")

    numero_match = re.search(regex_numeros, texto_relevante, re.VERBOSE)
    if numero_match:
        candidatos.append({'tipo': 'numero', 'pos': numero_match.start(), 'valor': numero_match.group(0)})
        print(f"Candidato numero encontrado: {numero_match.group(0)}")

    if not candidatos:
        print(f"Palabra clave: '{keyword_encontrada}'. No se encontró resultado válido en la zona acotada.")
        return None

    mejor_candidato = sorted(candidatos, key=lambda x: x['pos'])[0]
    
    if mejor_candidato['tipo'] == 'boxed':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
        print(f"Resultado (Prioridad: Boxed más cercano): {respuesta_final}")
        return respuesta_final
    elif mejor_candidato['tipo'] == 'latex':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
        print(f"Resultado (Prioridad: LaTeX más cercano): {respuesta_final}")
        return respuesta_final
    else: # tipo 'numero'
        respuesta_final = re.sub(r'^\*+|\*+$', '', mejor_candidato['valor']).strip()
        print(f"Resultado (Prioridad: Número más cercano): {respuesta_final}")
        return respuesta_final

# --- FUNCIÓN PARA PROCESAR EL CSV ---
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

            try:
                cabecera_original = next(csv_reader)
                csv_writer.writerow(cabecera_original + ['Respuesta Extraída'])
                fila_inicial = 2
            except StopIteration:
                csv_writer.writerow(['Texto Original', 'Respuesta Extraída'])
                infile.seek(0)
                fila_inicial = 1

            for i, fila in enumerate(csv_reader, start=fila_inicial):
                if not fila:
                    continue
                texto_a_procesar = fila[0]
                resultado = extraer_respuesta(texto_a_procesar, numero_fila=i)
                csv_writer.writerow(fila + [resultado if resultado is not None else ""])

        print(f"\n¡Proceso completado! Resultados guardados en '{archivo_salida}'")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    archivo_csv_entrada = "datos.csv"
    archivo_csv_salida = "resultados.csv"
    
    procesar_csv(archivo_csv_entrada, archivo_csv_salida)