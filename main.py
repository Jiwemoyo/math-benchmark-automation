import re

def extraer_resultado_numerico(texto):
    """
    Extrae solo el resultado numérico final de textos matemáticos complejos,
    ignorando fórmulas intermedias y capturando solo el número conclusivo.
    """
    # Limpiar el texto de LaTeX y formato
    texto_limpio = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', texto)  # Remover LaTeX básico
    texto_limpio = re.sub(r'\$+([^$]*)\$+', r'\1', texto_limpio)   # Remover $ de matemáticas
    texto_limpio = re.sub(r'\*\*([^*]*)\*\*', r'\1', texto_limpio) # Remover negritas
    
    patrones = [
        # Patrones con boxed (LaTeX)
        r'\\boxed\{(\d+(?:\.\d+)?)\}',
        
        # Patrones de respuesta final con palabras clave específicas
        r'(?:respuesta|resultado|conclusión|por lo tanto|finalmente|vale|mide)[^.]*?(\d+(?:\.\d+)?)[°°]?\s*[.\s]*$',
        
        # Patrones con "es" + número al final
        r'es[^.]*?(\d+(?:\.\d+)?)[°°]?\s*[.\s]*$',
        
        # Números en contextos de respuesta final
        r'(?:hay|son|existen?)[^.]*?(\d+(?:\.\d+)?)[^.]*?(?:enteros?|formas?|valores?|números?|puntos?)',
        
        # Números con unidades o contexto específico
        r'(\d+(?:\.\d+)?)\s*(?:personas?|enteros?|formas?|contenedores?|estaciones?|arreglos?|vértices?)',
        
        # Números después de "mínimo" o "máximo"
        r'(?:mínimo|máximo)[^.]*?(\d+(?:\.\d+)?)',
        
        # Números en fracciones comunes como respuesta final
        r'(\d+)/(\d+)',
        
        # Números decimales o enteros al final de párrafos
        r'(\d+(?:\.\d+)?)[°°]?\s*[.\s]*$',
        
        # Última línea con número
        r'\n[^.\n]*(\d+(?:\.\d+)?)[°°]?\s*[.\s]*$',
    ]
    
    # Buscar en todo el texto (incluyendo saltos de línea)
    for patron in patrones:
        try:
            matches = list(re.finditer(patron, texto_limpio, re.DOTALL | re.IGNORECASE))
            if matches:
                match = matches[-1]  # Tomar la última coincidencia
                if '/' in patron and match.lastindex == 2:  # Para fracciones
                    # Convertir fracción a decimal
                    num = float(match.group(1))
                    den = float(match.group(2))
                    return str(num/den) if den != 0 else match.group(1)
                return match.group(1)
        except (re.error, ValueError, ZeroDivisionError):
            continue  # Saltar patrones mal formados
    
    # Patrón de respaldo: buscar el último número en el texto
    numeros = re.findall(r'\b(\d+(?:\.\d+)?)\b', texto_limpio)
    if numeros:
        return numeros[-1]
    
    return None

def extraer_resultado_mejorado(texto):
    """
    Versión mejorada que combina múltiples estrategias
    """
    # Primero intentar con patrones específicos
    resultado = extraer_resultado_numerico(texto)
    if resultado:
        return resultado
    
    # Si no funciona, buscar en las últimas 3 líneas
    lineas = texto.strip().split('\n')
    for i in range(min(3, len(lineas))):
        linea = lineas[-(i+1)]
        numeros = re.findall(r'\b(\d+(?:\.\d+)?)\b', linea)
        if numeros:
            return numeros[-1]
    
    return None

# Ejemplos de uso con casos problemáticos específicos:
ejemplos_problematicos = [
    # Ejemplo 3 - debería extraer "0"
    """Por lo tanto:
$$\\lim_{t \\to \\infty} A_t = \\lim_{t \\to \\infty} \\frac{2}{t} = 0$$

**Respuesta final:** $\\boxed{0}$""",
    
    # Ejemplo 9 - debería extraer "0"  
    """**Conclusión**
Como $f'(x) > 0$ para todo $x$ real, la ecuación $f'(x) = 0$ no tiene soluciones reales.
Por lo tanto, el polinomio tiene **0 puntos críticos**.""",
    
    # Ejemplo 10 - debería extraer "4"
    """**Conclusión**
La suma de todas las raíces reales es: **4**""",
    
    # Ejemplo 21 - debería extraer "10"
    """**Conclusión**
La longitud del ciclo dirigido más grande en la digráfica es **10**."""
]

# Probar con los ejemplos problemáticos
print("Pruebas con casos problemáticos:")
for i, texto in enumerate(ejemplos_problematicos, 1):
    resultado = extraer_resultado_mejorado(texto)
    print(f"Ejemplo problemático {i}: {resultado}")

print("\n" + "="*50)

# Probar con todos los ejemplos originales
ejemplos = [
    """
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
    """, 
    """
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
    """, 
    """
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
    """,
    """
    "(r_1,r_2)$, $(r_2,r_3)$, $(r_3,r_4)$, $(r_4,r_5)$
- Similarmente, $h''(x)$ tiene al menos 3 raíces
- Y $h'''(x)$ tiene al menos 2 raíces

**Paso 6: Conclusión**
Como $g(x) = -e^{2x}h'''(x)$ y $e^{2x} > 0$ para todo $x \in \mathbb{R}$, las raíces de $g(x)$ son exactamente las raíces de $h'''(x)$.

Por lo tanto, el mínimo número de raíces reales distintas de $g(x) = f(x) + 6f'(x) + 12f''(x) + 8f'''(x)$ es **2**.

Este mínimo se alcanza, por ejemplo, cuando $f(x) = e^{2x}(x-1)(x-2)(x-3)(x-4)(x-5)$."
    """,
    """
    " regular.

Los únicos polígonos regulares que teselan el plano son:
- Triángulos (ángulo interno: 60°)
- Cuadrados (ángulo interno: 90°)
- Hexágonos (ángulo interno: 120°)

Para $n \geq 7$:
- El ángulo interno es $\frac{(n-2) \cdot 180°}{n} > 120°$
- No pueden teselar el plano
- No pueden formar empaquetamientos perfectos de un $n$-ágono
- ✗ No funciona

**Conclusión:**
Los únicos valores de $n$ que funcionan son $n = 3, 4, 6$.

Por lo tanto, hay **3** enteros positivos que cumplen la condición."
    """,
    """
    "olate):** 11

4. **Personas que les gusta fresa, chocolate y vainilla:** Este dato no se menciona explícitamente, pero según la información dada, no hay personas en esta categoría (el problema especifica que a las 8 personas les gusta fresa y chocolate, y a las 11 les gusta fresa y vainilla, sin mencionar un grupo que le gusten los tres).

**Total de personas a las que les gusta el helado de fresa:**
5 + 8 + 11 = **24 personas**

Por lo tanto, a 24 personas en total les gusta el helado de fresa."
    """,
    """
    " polígono tendría forma de ""dientes de sierra"" conectando todas las casillas blancas.

**Verificación:**
- Si Ana responde ""Sí"" → el punto está en una casilla blanca
- Si Ana responde ""No"" → el punto está en una casilla negra

**¿Por qué no se puede hacer con 0 preguntas?**
Sin hacer ninguna pregunta, Beto no tiene información sobre dónde está el punto, y hay igual probabilidad de que esté en una casilla blanca o negra.

**Conclusión:**
El mínimo número de preguntas que debe hacer Beto es **1**."
    """,
    """
    " Movimiento 3: Blancas eligen 1 de 3 peones restantes
- Movimiento 4: Negras eligen 1 de 3 peones restantes
- Movimiento 5: Blancas eligen 1 de 2 peones restantes
- Movimiento 6: Negras eligen 1 de 2 peones restantes
- Movimiento 7: Blancas mueven su último peón
- Movimiento 8: Negras mueven su último peón

El número de partidas diferentes es:
4 × 4 × 3 × 3 × 2 × 2 × 1 × 1 = 4! × 4! = 24 × 24 = **576**

**Respuesta:** Hay 576 partidas diferentes con movimientos legales que generan esta posición."
    """,
    """
    " 2x^3 + 3x^2 + 2x + 1$

Por lo tanto:
$$f'(x) = (x^2 + x + 1)^2 + 1$$

**Paso 5: Analizar las raíces**

Como $(x^2 + x + 1)^2 \geq 0$ para todo $x$ real, tenemos:
$$f'(x) = (x^2 + x + 1)^2 + 1 \geq 1 > 0$$

Esto significa que $f'(x)$ es siempre positivo para todo $x$ real.

**Conclusión**

Como $f'(x) > 0$ para todo $x$ real, la ecuación $f'(x) = 0$ no tiene soluciones reales.

Por lo tanto, el polinomio $f(x) = \frac{x^5}{5} + \frac{2x^4}{4} + x^3 + x^2 + 2x + 2025$ tiene **0 puntos críticos**."
    """,
    """
    "erificación**

Verifico sustituyendo $x = 4$ en la ecuación original:
$4^3 - 4(4^2) + 6(4) - 24 = 64 - 64 + 24 - 24 = 0$ ✓

**Conclusión**

La suma de todas las raíces reales es: **4**

Nota: También podría haber usado las relaciones de Vieta, que nos dicen que la suma de todas las raíces (reales y complejas) de $x^3 - 4x^2 + 6x - 24 = 0$ es $4$. Como las raíces complejas vienen en pares conjugados ($i\sqrt{6}$ y $-i\sqrt{6}$), su suma es $0$, confirmando que la suma de las raíces reales es $4$."
    """,
    """
    "ión queda $\frac{2x-2}{x-1} = x+3$, y $x = -1$ es solución.

Ambos valores de $k$ dan una única solución, pero el problema pide **el valor único** de $k$.

**Paso 8: Análisis adicional**

Revisando más cuidadosamente, cuando $k = -2$:
- $\frac{2x-2}{x-1} = \frac{2(x-1)}{x-1} = 2$ para $x \neq 1$
- Pero $x + 3 = 2$ implica $x = -1$
- Verificando: $\frac{2(-1)-2}{-1-1} = \frac{-4}{-2} = 2$ ✓

Por lo tanto, **$k = -2$** es el valor único que hace que la ecuación tenga exactamente una solución real."
    """,
    """
    "les no triviales cuando los coeficientes son fijos y no son potencias $n$-ésimas.

Específicamente, la ecuación $Ax^n + By^n = C$ con $A, B, C$ enteros positivos fijos y $n \geq 3$ tiene a lo más un número finito de soluciones racionales, y en la mayoría de los casos, no tiene soluciones no triviales.

**Conclusión:**

La única valor de $n$ para el cual existen enteros positivos $a$, $b$, $c$ satisfaciendo $2a^n + 3b^n = 4c^n$ es $n = 1$.

**La cantidad de todos los enteros positivos $n$ es 1.**"
    """,
    """
    "e satisfacen la condición es 6.**

Ejemplos que funcionan:
- $n = 6$: divisores 1, 2, 3 (suma = 6) ✓
- $n = 120$: divisores 8, 24, 40, 56 (suma = 128) ✗
- $n = 120$: divisores 3, 12, 21, 30, 39, 48 (no todos dividen)

De hecho, $n = 6$ con divisores 1, 2, 3 funciona.
$n = 12$ no funciona fácilmente.
$n = 18$ no funciona.
$n = 24$ no funciona.

Pero se puede verificar que hay infinitos múltiplos de 6 que funcionan, y ningún número que no sea múltiplo de 6 funciona.

Por lo tanto, el **MCD es 6**."
    """,
    """
    "lo si $\frac{x}{y} = 1$, es decir, $y = x$.

Por lo tanto, $g(x) = x$ y la condición de unicidad se cumple.

**Paso 8: Demostrar unicidad**

Supongamos que $f$ es una solución. De la ecuación $xf(g(x)) + g(x)f(x) = 2$, si $g(x) = x$ (lo cual probamos que debe ocurrir), entonces:
$$xf(x) + xf(x) = 2$$
$$2xf(x) = 2$$
$$f(x) = \frac{1}{x}$$

**Conclusión**

Existe una única función $f: \mathbb{R}^+ \to \mathbb{R}^+$ que satisface la condición dada, y es $f(x) = \frac{1}{x}$.

La respuesta es **1**."
    """,
    """
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
    """,
    """
    "

Para $s \geq 2$, el término $s^{2025}$ será mucho mayor que cualquier combinación posible del lado derecho.

**Paso 8: Verificar $r = -1$**
Probemos $r = -1$:
$$(-1)^{2025} + \sum_{i=1}^{2024}q_i (-1)^i + q_{2025} = -1 + \sum_{i=1}^{2024}q_i (-1)^i + q_{2025}$$

Esto da:
$$-1 + \sum_{i=1}^{1012}q_{2i} - \sum_{i=1}^{1012}q_{2i-1} + q_{2025}$$

Dado que los $q_i$ crecen muy rápidamente, esta suma no será cero.

**Conclusión:**
El polinomio dado no tiene raíces racionales.

La respuesta es **0**."
    """,
    """
    " 0$
Como $x$ es natural, $x = 0$ no es válido, y $x = -1$ tampoco.

**Caso 2:** $x^2 - x + 1 = 1$
Esto implica $x^2 - x = 0$, es decir $x(x - 1) = 0$
Como $x$ es natural, tenemos $x = 1$.

Cuando $x = 1$:
$x^4 + x^2 + 1 = 1 + 1 + 1 = 3$, que es primo.

Para cualquier $x > 1$, ambos factores $x^2 + x + 1$ y $x^2 - x + 1$ son mayores que 1, por lo que el producto no es primo.

**Respuesta:** Hay exactamente **1** número primo de la forma $x^4 + x^2 + 1$ con $x$ natural, y es el 3 (cuando $x = 1$)."
    """,
    """
    "iv 0 \pmod{6}$? Sí, $90 = 15 \cdot 6$

**Paso 4: Verificar que no hay soluciones menores**
Hemos verificado todas las ternas de primos consecutivos hasta $(7, 11, 13)$ y la primera que produce un $n$ divisible por 6 es esta última.

**Paso 5: Confirmar el resultado**
- $7, 11, 13$ son efectivamente primos consecutivos
- $n = 7 \cdot 11 + 13 = 77 + 13 = 90$
- $90 = 6 \cdot 15$, por lo tanto $6 | 90$ ✓

Por lo tanto, el menor entero positivo $n$ que satisface todas las condiciones es $\boxed{90}$."
    """,
    """
    "lizar el comportamiento cuando $x \to 0^+$**

De $f^2(x) = \frac{1}{x}$ y usando que $f^2(x) \leq k^2 f(x)$:
$$\frac{1}{x} \leq k^2 f(x)$$

Por lo tanto:
$$f(x) \geq \frac{1}{k^2 x}$$

Cuando $x \to 0^+$, tenemos $f(x) \to +\infty$.

**Paso 7: Determinar el límite pedido**

Como $f^{-1}(x) = \frac{1}{f(x)}$ y sabemos que cuando $x \to 0^+$, $f(x) \to +\infty$, entonces:

$$\lim_{x \to 0^+} f^{-1}(x) = \lim_{x \to 0^+} \frac{1}{f(x)} = 0$$

**Conclusión:**
$$\boxed{\lim_{x \to 0} f^{-1}(x) = 0}$$"
    """,
    """
    "

Evaluando:
- En x = 2.5: $\frac{3(2.5) - (2.5)^2/2}{2} = \frac{7.5 - 3.125}{2} = \frac{4.375}{2} = 2.1875$
- En x = 2: $\frac{3(2) - (2)^2/2}{2} = \frac{6 - 2}{2} = 2$

Por lo tanto: $P(2 \leq X \leq 2.5) = 2.1875 - 2 = 0.1875 = \frac{3}{16}$

**Paso 6: Respuesta final**

La probabilidad de que la demanda esté entre 0 y 0.5 kg o entre 2 y 2.5 kg es:

$$P = P(0 \leq X \leq 0.5) + P(2 \leq X \leq 2.5) = \frac{1}{16} + \frac{3}{16} = \frac{4}{16} = \frac{1}{4}$$

**La probabilidad es 0.25 o 25%**"
    """,
    """
    "B (9 líneas)

**Paso 4: Identificar líneas que requieren 2 o más transbordos**
Las líneas no directamente conectadas a la Línea 1:
- **Línea 2** (Azul)
- **Línea 6** (Rojo)
- **Línea 12** (Dorado)

**Paso 5: Contar las estaciones**

Línea 2: 24 estaciones (Cuatro Caminos a Tasqueña)
Línea 6: 11 estaciones (El Rosario a Martín Carrera)
Línea 12: 20 estaciones (Mixcoac a Tláhuac)

**Total: 24 + 11 + 20 = 55 estaciones**

**Respuesta: 55 estaciones requieren al menos 2 transbordos desde Balbuena.**"
    """,
    """
    "s)
- Los vértices de partes diferentes deben tener colores diferentes (están todos conectados)
- Por lo tanto, necesitamos exactamente r colores

## Paso 5: Aplicar al problema
En nuestro caso, T(13,4) tiene número cromático χ = 4.

Esto significa que:
- Las flores se pueden organizar en 4 grupos
- Las flores dentro de cada grupo son compatibles entre sí
- Las flores de grupos diferentes son incompatibles

**Respuesta: La florista necesita un mínimo de 4 contenedores para organizar sus flores.**"
    """,
    """
    "lo tanto, Marketing DEBE hacer ventas

Con RRHH haciendo planeación estratégica y Marketing haciendo ventas:
- Ingeniería NO puede hacer planeación estratégica ni ventas (ya están asignadas)
- Ingeniería puede hacer: I+D o gestión de activos

**Paso 4: Contar las formas de asignación**

1. RRHH → Planeación estratégica, Marketing → Ventas, Ingeniería → I+D
2. RRHH → Planeación estratégica, Marketing → Ventas, Ingeniería → Gestión de activos

**Respuesta: Existen 2 formas de asignar las tareas.**"
    """,
    """
    "3$:**
- $\deg(i,x) = \deg_{P_4}(i) + \deg_{K_3}(x)$

## Paso 4: Determinar los grados de todos los vértices

- $(1,a), (1,b), (1,c)$: grado $1 + 2 = 3$
- $(2,a), (2,b), (2,c)$: grado $2 + 2 = 4$
- $(3,a), (3,b), (3,c)$: grado $2 + 2 = 4$
- $(4,a), (4,b), (4,c)$: grado $1 + 2 = 3$

## Paso 5: Identificar el grado máximo

El grado máximo en $P_4 \square K_3$ es **4**.

Los vértices con grado máximo son:
- $(2,a), (2,b), (2,c), (3,a), (3,b), (3,c)$

Por lo tanto, hay **6 vértices** de grado máximo."
    """,
    """
    "cesitamos perder una intersección más.

**Paso 8: Configuración óptima**
Podemos tener:
- 3 rectas paralelas entre sí
- 2 rectas paralelas entre sí (pero no a las primeras 3)
- 1 recta no paralela a ninguna

Intersecciones:
- Las 3 paralelas no se intersectan: 0
- Las 2 paralelas no se intersectan: 0
- La recta solitaria intersecta a las otras 5: 5
- Las 3 paralelas intersectan a las 2 paralelas: 3×2 = 6
- Total: 5 + 6 = 11 ✓

**Respuesta: El máximo número de rectas paralelas en el plano es 3.**"
    """,
    """
    " color falta en una ventana de 8, debe aparecer inmediatamente después en las siguientes 2 posiciones.

Analizando cuidadosamente esta restricción:
- Si el color $c$ falta en $W_i$, aparece en $i+8$ y $i+9$
- Entonces $c$ no puede faltar en $W_{i+1}$ (porque contiene a $i+8$)
- Ni en $W_{i+2}$ (porque contiene a $i+8$ y $i+9$)

Esto genera un patrón que eventualmente se contradice al dar la vuelta completa a la circunferencia de 50 puntos.

**Conclusión:**

El mínimo valor de $l$ es $\boxed{8}$."
    """,
    """
    ")$ con $i+j > k+l$, entonces no podemos volver a una entrada con suma $\geq i+j$ sin usar múltiples pasos horizontales.
- Cualquier intento de crear un ciclo más largo requeriría ""bajar"" en suma de índices y luego ""subir"", lo cual es imposible solo con la regla 2.

**Conclusión**

La longitud del ciclo dirigido más grande en la digráfica es **10**.

Este ciclo se forma siguiendo cualquier entrada fija $(i,j)$ a través de las 10 matrices consecutivas usando solo la regla 1 (aristas horizontales)."
    """,
    """
    " (par)

Solo tenemos un número con frecuencia impar (el 0), lo cual hace imposible formar una cadena que use todas las fichas.

**Conclusión**: No es posible formar ningún arreglo que use todas las fichas siguiendo las reglas del dominó.

La respuesta es **0 arreglos distintos**.

Esto se debe a que para formar una cadena válida de dominó, necesitamos que haya exactamente 0 o 2 números con frecuencia impar (los extremos de la cadena), pero en este caso tenemos solo 1 número con frecuencia impar."
    """,
    """
    " Bazar a las 14hrs, Proyección a las 18hrs
- Bazar en Salón (14hrs) + Proyección en Salón (18hrs) ✓
- Bazar en Salón (14hrs) + Proyección en Auditorio (18hrs) ✓
- Bazar en Auditorio (14hrs) + Proyección en Salón (18hrs) ✓
- Bazar en Auditorio (14hrs) + Proyección en Auditorio (18hrs) ✓

Total Caso 2: **6 formas**

**Respuesta final: 8 + 6 = 14 formas**

Existen **14 formas diferentes** de asignar los espacios y horarios para que las actividades no se realicen en el mismo espacio al mismo tiempo."
    """
]

print("Pruebas con ejemplos originales:")
for i, texto in enumerate(ejemplos, 1):
    resultado = extraer_resultado_mejorado(texto)
    print(f"Ejemplo original {i}: {resultado}")