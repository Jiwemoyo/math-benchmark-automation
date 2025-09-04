import re

# --- Textos de Ejemplo ---
texto_ejemplo_1 = r"**Respuesta: El ángulo $ABC$ mide $55°$**"
texto_ejemplo_2 = r"**Respuesta: El ángulo DPA vale 37.5°**"
texto_ejemplo_3 = r"**Respuesta final:** $\boxed{0}$"
texto_ejemplo_4 = r"Tras los cálculos, es decir, la respuesta es 55° y no otra."
texto_ejemplo_5 = r"La respuesta es 10 y el ángulo es 45°"
texto_ejemplo_6 = r"El resultado de la división es 3/4, por lo tanto es la respuesta correcta."
texto_ejemplo_7 = r"**Respuesta final:** La probabilidad es **1** (o 100%)."
texto_ejemplo_8 = r"La solución de la ecuación es \boxed{x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}}"
texto_ejemplo_9 = r"Por lo tanto, el valor del ángulo es $\alpha = 45°$."
texto_ejemplo_10 = r"""
" polígono tendría forma de ""dientes de sierra"" conectando todas las casillas blancas.

**Verificación:**
- Si Ana responde ""Sí"" → el punto está en una casilla blanca
- Si Ana responde ""No"" → el punto está en una casilla negra

**¿Por qué no se puede hacer con 0 preguntas?**
Sin hacer ninguna pregunta, Beto no tiene información sobre dónde está el punto, y hay igual probabilidad de que esté en una casilla blanca o negra.

**Conclusión:**
El mínimo número de preguntas que debe hacer Beto es **1**."
"""

texto_ejemplo_11 = r"""

"""

def to_inline_mode(latex_str):
    # Extraer contenido de \boxed{...}
    latex_str = re.sub(r'\\boxed\{(.+?)\}', r'\1', latex_str)
    # Quitar $$ ... $$ y $ ... $
    latex_str = re.sub(r'\$\$?(.+?)\$\$?', r'\1', latex_str)
    # Envolver en $ ... $
    return f"${latex_str.strip()}$"

# --- Configuración del Extractor ---
palabras_clave = [
    "Respuesta Final", "Respuesta", "Por lo tanto", "Conclusión", 
    "Resultado final", "Es decir", "La solución de la ecuación es",
    "El resultado de la división es", "el valor del ángulo es"
]
palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

# Regex separadas por prioridad
regex_boxed = r'\\boxed\{.*\s*\}'  # Prioridad 1
regex_latex_otros = r'\$\$.*?\$\$|\$[^$]*\$'
regex_numeros = r'\*{2}\s*-?(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?\s*\*{2}|-?\b(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?\b'

# --- FUNCIÓN DE EXTRACCIÓN ---
def extraer_respuesta(texto):
    print(f"--- Procesando texto {ejemplos.index(texto) + 1} ---")

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

# --- Pruebas de la Función ---
print("Resultados de la extracción (con normalización LaTeX):")
ejemplos = [
    texto_ejemplo_1, texto_ejemplo_2, texto_ejemplo_3, texto_ejemplo_4,
    texto_ejemplo_5, texto_ejemplo_6, texto_ejemplo_7, texto_ejemplo_8,
    texto_ejemplo_9, texto_ejemplo_10, texto_ejemplo_11
]
resultados = [extraer_respuesta(texto) for texto in ejemplos]

print("\n--- Resumen de resultados finales (normalizados) ---")
for i, res in enumerate(resultados, 1):
    print(f"Texto {i}: {res}")

# Pruebas adicionales de la función to_inline_mode
print("\n--- Pruebas de la función to_inline_mode ---")
print(to_inline_mode(r'$55°$'))  
print(to_inline_mode(r'$55$'))              
print(to_inline_mode(r'$$\boxed{Peso_{cilindro} = \frac{p\sqrt{3}}{3} \text{ kg}}$$'))
print(to_inline_mode(r'\boxed{\frac{1}{2}}'))
print(to_inline_mode(r'$$x = 5$$'))