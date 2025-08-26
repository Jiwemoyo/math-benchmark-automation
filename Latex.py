import re

def find_final_latex_expression(text):
    r"""
    Encuentra la expresión LaTeX que aparece después de palabras clave específicas
    como 'Respuesta final', 'Por lo tanto', 'Conclusión', etc.
    """
    # Palabras clave que indican la respuesta final
    keywords = [
        r'Respuesta final',
        r'Respuesta',
        r'Por lo tanto',
        r'Conclusión',
        r'Resultado final', 
        r'Es decir',
        r'En conclusión'
    ]
    
    # Pattern para encontrar expresiones LaTeX
    latex_pattern = r'(?<!\\)\$(.*?)(?<!\\)\$|(?<!\\)\$\$(.*?)(?<!\\)\$\$|\\\[(.*?)\\\]'
    
    # Buscar todas las ocurrencias de palabras clave
    for keyword in keywords:
        # Encontrar la posición de la palabra clave
        keyword_match = re.search(keyword, text, re.IGNORECASE)
        if keyword_match:
            # Obtener el texto después de la palabra clave
            text_after_keyword = text[keyword_match.end():]
            
            # Buscar la primera expresión LaTeX después de la palabra clave
            latex_match = re.search(latex_pattern, text_after_keyword, re.DOTALL)
            if latex_match:
                # Extraer la expresión LaTeX (puede estar en cualquier grupo)
                latex_expr = next((group for group in latex_match.groups() if group), None)
                if latex_expr:
                    return latex_expr.strip()
    
    # Si no se encuentra después de palabras clave, devolver la última expresión
    all_expressions = re.findall(latex_pattern, text, re.DOTALL)
    if all_expressions:
        # Obtener la última expresión encontrada
        last_expr = [exp for group in all_expressions[-1] for exp in [group] if exp]
        if last_expr:
            return last_expr[0].strip()
    
    return None

# Tu texto
texto = r"""
Voy a resolver este problema paso a paso.

**Datos dados:**
- Área lateral del cono: $A_L = 100 \text{ u}^2$
- Área total del cono: $A_T = 140 \text{ u}^2$

**Paso 1: Identificar las fórmulas relevantes**

Para un cono de revolución:
- Área lateral: $A_L = \pi r g$
- Área total: $A_T = \pi r g + \pi r^2$
- Área de la base: $A_B = \pi r^2$

Donde:
- $r$ = radio de la base
- $g$ = generatriz
- $h$ = altura

**Paso 2: Encontrar el área de la base**

Como $A_T = A_L + A_B$, entonces:
$$A_B = A_T - A_L = 140 - 100 = 40 \text{ u}^2$$

**Paso 3: Establecer relaciones**

De las fórmulas:
- $\pi r g = 100$ ... (1)
- $\pi r^2 = 40$ ... (2)

**Paso 4: Encontrar la relación entre g y r**

Dividiendo la ecuación (1) entre la ecuación (2):
$$\frac{\pi r g}{\pi r^2} = \frac{100}{40}$$
$$\frac{g}{r} = \frac{5}{2}$$
$$g = \frac{5r}{2}$$

**Paso 5: Encontrar los valores de r y g**

De la ecuación (2):
$$\pi r^2 = 40$$
$$r^2 = \frac{40}{\pi}$$
$$r = \sqrt{\frac{40}{\pi}} = \frac{2\sqrt{10}}{\sqrt{\pi}}$$

Sustituyendo en $g = \frac{5r}{2}$:
$$g = \frac{5}{2} \cdot \frac{2\sqrt{10}}{\sqrt{\pi}} = \frac{5\sqrt{10}}{\sqrt{\pi}}$$

**Paso 6: Encontrar el ángulo entre la generatriz y la altura**

En un cono, la generatriz, la altura y el radio forman un triángulo rectángulo donde:
- La generatriz es la hipotenusa
- La altura y el radio son los catetos
- El ángulo $\alpha$ entre la generatriz y la altura satisface:

$$\sin \alpha = \frac{r}{g}$$

Sustituyendo la relación encontrada:
$$\sin \alpha = \frac{r}{g} = \frac{1}{\frac{5}{2}} = \frac{2}{5}$$

Por lo tanto:
$$\alpha = \arcsin\left(\frac{2}{5}\right)$$

**Respuesta final:**

El ángulo que forma la generatriz con la altura es:
$$\alpha = \arcsin\left(\frac{2}{5}\right) \approx 23.58°$$
"""

# Encontrar la expresión final
expresion_final = find_final_latex_expression(texto)

print("Expresión LaTeX final encontrada:")
print(expresion_final)



ejemplos_latex =[
    """
    """,
    """
    """,
]