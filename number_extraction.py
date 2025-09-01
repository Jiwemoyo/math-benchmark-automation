import re


texto_ejemplo_1 = r"""
"**Respuesta: El ángulo $ABC$ mide 55°**"
"""

texto_ejemplo_2 = r"""
"**Respuesta: El ángulo DPA vale 37.5°**"
"""

texto_ejemplo_3 = r"""
"Por lo tanto:
$$\lim_{t \to \infty} A_t = \lim_{t \to \infty} \frac{2}{t} = 0$$

**Respuesta final:** $\boxed{0}$"
"""

texto_ejemplo_4 = r"Tras los cálculos, es decir, la respuesta es 55° y no otra."
texto_ejemplo_5 = r"La respuesta es \boxed{x = 10} y el ángulo es 45°"
texto_ejemplo_6 = r"El resultado de la división es 3/4, por lo tanto es la respuesta correcta."


texto_ejemplo_7 = r"""
"olate):** 11

4. **Personas que les gusta fresa, chocolate y vainilla:** Este dato no se menciona explícitamente, pero según la información dada, no hay personas en esta categoría (el problema especifica que a las 8 personas les gusta fresa y chocolate, y a las 11 les gusta fresa y vainilla, sin mencionar un grupo que le gusten los tres).

**Total de personas a las que les gusta el helado de fresa:**
5 + 8 + 11 = **24 personas**

Por lo tanto, a -7 personas en total les gusta el helado de fresa."
"""

# --- Configuración del Extractor ---

# Palabras claves
palabras_clave = [
    "Respuesta Final",
    "Respuesta",
    "Por lo tanto",
    "Conclusion",
    "Resultado final",
    "Es decir"
]

palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

# Regex actualizada:
# Busca un número dentro de **...** O un número plano.
# El patrón tiene dos grupos de captura principales, uno para cada caso.
regex_numeros_actualizada = r'\*{2}\s*(-?(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?)\s*\*{2}|(-?\b(?:\d+\s*/\s*\d+|\d+(?:\.\d+)?)\°?\b)'


def extraer_resultados_numericos(texto, patron_keywords, regex_numeros):
    """
    Busca una palabra clave y extrae el primer resultado numérico que la sigue,
    ya sea plano o encerrado en dobles asteriscos.
    """
    print(f"--- Procesando texto ---")
    print(f"Texto original: \"{texto.strip()[:70]}...\"")

    match = re.search(patron_keywords, texto, re.IGNORECASE)

    if match:
        keyword_encontrada = match.group(0)
        texto_relevante = texto[match.end():]
        
        numeros_match = re.search(regex_numeros, texto_relevante)
        
        if numeros_match:
            # La regex tiene dos grupos de captura: uno para el caso (**num**) y otro para el caso (num).
            # El resultado correcto será el grupo que no sea 'None'.
            # Usamos filter para eliminar el 'None' y next para obtener el primer (y único) resultado.
            try:
                resultado = next(filter(None, numeros_match.groups())).strip()
                print(f"Palabra clave encontrada: '{keyword_encontrada}'")
                print(f"Resultado numérico extraído: {resultado}")
                return resultado
            except StopIteration:
                pass

        print(f"Palabra clave encontrada: '{keyword_encontrada}', pero no se encontró un resultado numérico después.")
        return None
    else:
        print("No se encontró ninguna de las palabras clave en el texto.")
        return None

# --- Pruebas de la Función Actualizada ---

print("Resultados de la extracción (incluyendo números con **):")
resultados = []
resultados.append(extraer_resultados_numericos(texto_ejemplo_1, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_2, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_3, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_4, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_5, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_6, patron_keywords, regex_numeros_actualizada))
resultados.append(extraer_resultados_numericos(texto_ejemplo_7, patron_keywords, regex_numeros_actualizada)) 

print("\n--- Resumen de resultados finales ---")
for i, res in enumerate(resultados, 1):
    print(f"Texto {i}: {res}")