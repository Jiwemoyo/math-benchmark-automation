import re

# --- Textos de Ejemplo ---
texto_ejemplo_1 = r"""
"
La razón de volúmenes es:
$$\frac{V_{cilindro,max}}{V_{esfera}} = \frac{\frac{4\pi R^3}{3\sqrt{3}}}{\frac{4\pi R^3}{3}} = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$$

Como ambos objetos tienen la misma densidad (mismo material):
$$\frac{Peso_{cilindro}}{Peso_{esfera}} = \frac{V_{cilindro,max}}{V_{esfera}} = \frac{\sqrt{3}}{3}$$

## Respuesta final

El peso del mayor cilindro circular recto que puede cortarse de la esfera es:

$$\boxed{Peso_{cilindro} = \frac{p\sqrt{3}}{3} \text{ kg}}$$"
"""
texto_ejemplo_2 = r"**Respuesta: El ángulo DPA vale 37.5°**"
texto_ejemplo_3 = r"**Respuesta final:** $\boxed{0}$"
texto_ejemplo_4 = r"Tras los cálculos, es decir, la respuesta es 55° y no otra."
texto_ejemplo_5 = r"La respuesta es 10 y el ángulo es 45°"
texto_ejemplo_6 = r"El resultado de la división es 3/4, por lo tanto es la respuesta correcta."
texto_ejemplo_7 = r"**Respuesta final:** La probabilidad es **1** (o 100%)."
texto_ejemplo_8 = r"La solución de la ecuación es \boxed{x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}}"
texto_ejemplo_9 = r"Por lo tanto, el valor del ángulo es $\alpha = 45°$."
texto_ejemplo_10 = r"""**Conclusión:** El mínimo número de preguntas que debe hacer Beto es **1**."""

# Tu nuevo ejemplo clave
texto_ejemplo_11 = r"""
"(r_1,r_2)$, $(r_2,r_3)$, $(r_3,r_4)$, $(r_4,r_5)$
- Similarmente, $h''(x)$ tiene al menos 3 raíces
- Y $h'''(x)$ tiene al menos 2 raíces

**Paso 6: Conclusión**
Como $g(x) = -e^{2x}h'''(x)$ y $e^{2x} > 0$ para todo $x \in \mathbb{R}$, las raíces de $g(x)$ son exactamente las raíces de $h'''(x)$.

Por lo tanto, el mínimo número de raíces reales distintas de $g(x) = f(x) + 6f'(x) + 12f''(x) + 8f'''(x)$ es **2**.

Este mínimo se alcanza, por ejemplo, cuando $f(x) = e^{2x}(x-1)(x-2)(x-3)(x-4)(x-5)$.
"""

# Texto con múltiples palabras clave (nuevo ejemplo)
texto_ejemplo_12 = r"""
"1, 2, 3, ..., 504\}$:
- $k = 4j$
- $m$ puede tomar valores desde 2 hasta $2020 - 4j$
- El número de valores posibles de $m$ es: $(2020 - 4j) - 2 + 1 = 2019 - 4j$

El número total de enteros $N$ es:
$$\sum_{j=1}^{504} (2019 - 4j) = \sum_{j=1}^{504} 2019 - 4\sum_{j=1}^{504} j$$

$$= 504 \times 2019 - 4 \times \frac{504 \times 505}{2}$$

$$= 504 \times 2019 - 4 \times 127260$$

$$= 1017576 - 509040$$

$$= 508536$$

Por lo tanto, hay **508,536** enteros positivos que satisfacen las tres condiciones."
"""

# Función to_inline_mode simplificada y corregida
def to_inline_mode(latex_str):
    content = latex_str
    # Usar regex para extraer contenido de \boxed de forma segura
    # Esta regex maneja un nivel de llaves anidadas
    boxed_match = re.search(r'\\boxed\{(.*)\}', content, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
    
    # Quitar delimitadores $$ o $ de los bordes
    content = re.sub(r'^\$\$?|\$\$?$', '', content).strip()
    return f"${content}$"

# --- Configuración del Extractor ---
palabras_clave = [
    "Respuesta Final", "Respuesta", "Por lo tanto", "Conclusión", 
    "Resultado final", "Es decir", "La solución de la ecuación es",
    "El resultado de la división es", "el valor del ángulo is"
]
palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

patron_secundario = r'\b(es|son|vale|mide|sea|es el|es la)\b\s*:?'

# Regex de formatos de respuesta - SIMPLIFICADA Y CORREGIDA
# Esta regex para boxed maneja correctamente llaves anidadas
regex_boxed = r'\\boxed\{(?:[^{}]|{[^{}]*})*\}' 
regex_latex_otros = r'\$\$.*?\$\$|\$[^$]*\$'

# REGEX MEJORADA PARA NÚMEROS - AHORA CAPTURA FRACCIONES CORRECTAMENTE
regex_numeros = r'''
    # Números con comas (508,536)
    \b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|
    # Números con puntos (508.536)  
    \b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|
    # Números en negrita doble (**2**, **508,536**)  ← ESTA LÍNEA
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

# --- FUNCIÓN DE EXTRACCIÓN ---
def extraer_respuesta(texto):
    if not texto or texto.isspace():
        print(f"--- Procesando texto {ejemplos.index(texto) + 1}: Vacío ---")
        return None
        
    print(f"--- Procesando texto {ejemplos.index(texto) + 1} ---")

    # MODIFICACIÓN: Buscar TODAS las ocurrencias y tomar la ÚLTIMA
    todas_keywords = list(re.finditer(patron_keywords, texto, re.IGNORECASE))
    if not todas_keywords:
        print("No se encontró palabra clave principal.")
        return None
    
    # Tomar la última ocurrencia de palabra clave
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
    
    # Buscar el primer candidato de cada tipo y guardar su posición
    boxed_match = re.search(regex_boxed, texto_relevante, re.DOTALL)
    if boxed_match:
        candidatos.append({'tipo': 'boxed', 'pos': boxed_match.start(), 'valor': boxed_match.group(0)})
        print(f"Candidato boxed encontrado: {boxed_match.group(0)}")

    latex_match = re.search(regex_latex_otros, texto_relevante, re.DOTALL)
    if latex_match:
        candidatos.append({'tipo': 'latex', 'pos': latex_match.start(), 'valor': latex_match.group(0)})
        print(f"Candidato latex encontrado: {latex_match.group(0)}")

    # Usar re.VERBOSE para la regex mejorada de números
    numero_match = re.search(regex_numeros, texto_relevante, re.VERBOSE)
    if numero_match:
        candidatos.append({'tipo': 'numero', 'pos': numero_match.start(), 'valor': numero_match.group(0)})
        print(f"Candidato numero encontrado: {numero_match.group(0)}")

    if not candidatos:
        print(f"Palabra clave: '{keyword_encontrada}'. No se encontró resultado válido en la zona acotada.")
        return None

    # Ordenar los candidatos por su posición de inicio y elegir el primero (el más cercano)
    mejor_candidato = sorted(candidatos, key=lambda x: x['pos'])[0]
    
    # Procesar el candidato ganador según su tipo
    if mejor_candidato['tipo'] == 'boxed':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado (Prioridad 1: Boxed más cercano):")
        return respuesta_final
    elif mejor_candidato['tipo'] == 'latex':
        respuesta_final = to_inline_mode(mejor_candidato['valor'])
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado (Prioridad 2: LaTeX más cercano):")
        return respuesta_final
    else: # tipo 'numero'
        # Limpiar el número: quitar asteriscos al principio y final, pero mantener comas y fracciones
        respuesta_final = re.sub(r'^\*+|\*+$', '', mejor_candidato['valor']).strip()
        print(f"Palabra clave: '{keyword_encontrada}'. Resultado (Prioridad 3: Número más cercano):")
        return respuesta_final

# --- Pruebas de la Función ---
print("Resultados de la extracción (Lógica 'El Más Cercano Gana' + Última palabra clave):")
ejemplos = [
    texto_ejemplo_1, texto_ejemplo_2, texto_ejemplo_3, texto_ejemplo_4,
    texto_ejemplo_5, texto_ejemplo_6, texto_ejemplo_7, texto_ejemplo_8,
    texto_ejemplo_9, texto_ejemplo_10, texto_ejemplo_11, texto_ejemplo_12
]
resultados = [extraer_respuesta(texto) for texto in ejemplos]

print("\n--- Resumen de resultados finales ---")
for i, res in enumerate(resultados, 1):
    print(f"Texto {i}: {res}")