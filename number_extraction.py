import re

# Añadimos la 'r' antes de las tres comillas
texto = r""" "= \angle CBA$

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

regex_numerico  = r'-?\b\d+(?:\.\d+)?°?\b'
palabra_clave = "respuesta"
partes_del_texto = texto.split(palabra_clave,1)

if len(partes_del_texto) > 1:
    # La segunda parte (índice 1) es el texto que nos interesa
    texto_relevante = partes_del_texto[1]
    
    # Ahora aplicamos findall solo a esta nueva porción de texto
    numero_extraido = re.findall(regex_numerico, texto_relevante)
    
    print("Texto después de la palabra clave:", texto_relevante.strip())
    print("Número(s) extraído(s):", numero_extraido)
else:
    print(f"La palabra clave '{palabra_clave}' no fue encontrada en el texto.")