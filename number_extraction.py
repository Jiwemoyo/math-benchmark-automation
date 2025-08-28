import re

texto_ejemplo_1 = r"""
" = \angle CBA$

Usando que la suma de ángulos en un triángulo es $180°$:
$\angle CAB + \angle CBA + \angle ACB = 180°$

Como $\angle CAB = \angle CBA$:
$2 \cdot \angle CBA + 70° = 180°$
$2 \cdot \angle CBA = 110°$
$\angle CBA = 55°$

**Verificación:**

Podemos verificar que nuestra solución es consistente:
- En el triángulo $ADC$: $AD = AC$ (isósceles)
- En el triángulo $ABC$: $AC = BC$ (isósceles)
- Por lo tanto: $AD = BC$ ✓ (coincide con el dato dado)

**Respuesta: El ángulo $ABC$ mide $55°$**"
"""

texto_ejemplo_2 = r"""
" 5: Aplicar el teorema del ángulo tangente-cuerda**

Hay otra forma de ver este problema. El ángulo ∠DPA es un ángulo exterior formado por la tangente PD y la secante PA.

Por el teorema del ángulo formado por una tangente y una secante desde un punto exterior:

∠DPA = ½|arco AD - arco BD|

Donde:
- Arco AD = 130° (ángulo central ∠AOD)
- Arco BD = 55° (ángulo central ∠BOD)

**Paso 6: Calcular el resultado**

∠DPA = ½|130° - 55°|
∠DPA = ½(75°)
∠DPA = 37.5°

**Respuesta: El ángulo DPA vale 37.5°**"
"""

texto_ejemplo_3 = r"""
"2tu + u^2$$

La condición $t^2 - 1 \leq x^2 \leq t^2 + 1$ se convierte en:
$$-1 \leq 2tu + u^2 \leq 1$$

Para $t$ grande, $u^2$ es despreciable comparado con $2tu$, así que:
$$-1 \leq 2tu \leq 1$$
$$-\frac{1}{2t} \leq u \leq \frac{1}{2t}$$

**Paso 8: Calcular el límite**

El área es aproximadamente:
$$A_t \approx \int_{-1/(2t)}^{1/(2t)} 2 \, du = 2 \cdot \frac{2}{2t} = \frac{2}{t}$$

Por lo tanto:
$$\lim_{t \to \infty} A_t = \lim_{t \to \infty} \frac{2}{t} = 0$$

**Respuesta final:** $\boxed{0}$"
"""

texto_ejemplo_4 = r"""
" \frac{2\sqrt{2} + 4 + 2 + 2\sqrt{2}}{\sqrt{2}}]$
$y = a[1 + \frac{4\sqrt{2} + 6}{\sqrt{2}}]$
$y = a[1 + 4 + \frac{6}{\sqrt{2}}]$
$y = a[5 + 3\sqrt{2}]$

Por tanto, $T = (-a\frac{\sqrt{2} + 2}{\sqrt{2}}, a(5 + 3\sqrt{2}))$

**Paso 7: Calcular $PT$**

$P = (-a\frac{\sqrt{2} + 2}{\sqrt{2}}, 0)$ y $T = (-a\frac{\sqrt{2} + 2}{\sqrt{2}}, a(5 + 3\sqrt{2}))$

Como ambos puntos tienen la misma coordenada $x$:
$PT = |a(5 + 3\sqrt{2}) - 0| = a(5 + 3\sqrt{2})$

Por lo tanto, $\boxed{PT = a(5 + 3\sqrt{2})}$"
"""
texto_ejemplo_5 = r"""
"2tu + u^2$$

La condición $t^2 - 1 \leq x^2 \leq t^2 + 1$ se convierte en:
$$-1 \leq 2tu + u^2 \leq 1$$

Para $t$ grande, $u^2$ es despreciable comparado con $2tu$, así que:
$$-1 \leq 2tu \leq 1$$
$$-\frac{1}{2t} \leq u \leq \frac{1}{2t}$$

**Paso 8: Calcular el límite**

El área es aproximadamente:
$$A_t \approx \int_{-1/(2t)}^{1/(2t)} 2 \, du = 2 \cdot \frac{2}{2t} = \frac{2}{t}$$

Por lo tanto:
$$\lim_{t \to \infty} A_t = \lim_{t \to \infty} \frac{2}{t} = 0$$

**Respuesta final:** $\boxed{0}$"
"""

# Palabras claves más comunes que usan los modelos 
palabras_clave = [
    "Respuesta Final",
    "Respuesta",
    "Por lo tanto",
    "Conclusion", 
    "Resultado final",
    "Es decir"
]

# Ordenar por longitud para que se pueda comparar correctamente
palabras_clave.sort(key=len, reverse=True)
patron_keywords = '|'.join(re.escape(palabra) for palabra in palabras_clave)

# regex para encontrar números 
regex_numeros = r'-?\b\d+(?:\.\d+)?\°?\b'
regex_boxed = r'\\boxed\{([^}]*)\}'

def extraer_resultados(texto, patron_keywords, regex_boxed, regex_numeros):
    print(f"--- Procesando texto ---")
    print(f"Texto original: \"{texto[:60]}...\"")
    
    match = re.search(patron_keywords, texto, re.IGNORECASE)
    
    if match:
        keyword_encontrada = match.group(0)
        indice_final = match.end()
        texto_relevante = texto[indice_final:]
        
        # Primero buscar \boxed{} (tiene prioridad)
        boxed_match = re.search(regex_boxed, texto_relevante)
        if boxed_match:
            resultado = boxed_match.group(1)
            print(f"Palabra clave encontrada: '{keyword_encontrada}'")
            print(f"Resultado extraído de \\boxed{{}}: {resultado}")
            return resultado
        
        # Si no hay \boxed{}, buscar números sueltos
        numeros_match = re.search(regex_numeros, texto_relevante)
        if numeros_match:
            resultado = numeros_match.group(0)
            print(f"Palabra clave encontrada: '{keyword_encontrada}'")
            print(f"Resultado extraído (número suelto): {resultado}")
            return resultado
        
        print(f"Palabra clave encontrada: '{keyword_encontrada}', pero no se encontró resultado")
        return None
    else:
        print("No se encontró ninguna de las palabras clave en el texto.")
        return None
    print("-" * 25)

# Probar la función corregida
print("Resultados con prioridad para \\boxed{}:")
resultados = []
resultados.append(extraer_resultados(texto_ejemplo_1, patron_keywords, regex_boxed, regex_numeros))
resultados.append(extraer_resultados(texto_ejemplo_2, patron_keywords, regex_boxed, regex_numeros))
resultados.append(extraer_resultados(texto_ejemplo_3, patron_keywords, regex_boxed, regex_numeros))
resultados.append(extraer_resultados(texto_ejemplo_4, patron_keywords, regex_boxed, regex_numeros))
resultados.append(extraer_resultados(texto_ejemplo_5, patron_keywords, regex_boxed, regex_numeros))

print("\nResultados finales extraídos:")
for i, res in enumerate(resultados, 1):
    print(f"Texto {i}: {res}")