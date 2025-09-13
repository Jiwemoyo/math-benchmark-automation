import re
from .normalizer import to_inline_mode

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
