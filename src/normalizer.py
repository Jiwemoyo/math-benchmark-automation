import re
import unicodedata
import sympy as sp
from sympy import simplify, symbols, N
from decimal import Decimal, InvalidOperation

def to_inline_mode(latex_str):
    content = latex_str
    boxed_match = re.search(r'\\boxed\{(.*)\}', content, re.DOTALL)
    if boxed_match:
        content = boxed_match.group(1)
    content = re.sub(r'^\$\$?|\$\$?$', '', content).strip()
    return f"${content}$"

def is_math_expression(text):
    """Detecta si el texto parece una expresión matemática"""
    if not isinstance(text, str):
        return False
    
    math_indicators = [
        r'\\frac', r'\\sqrt', r'\\boxed', r'^\\', r'\^', r'_',
        r'\{', r'\}', r'\\begin', r'\\end', r'\\cdot', r'\\times',
        r'\$(.*?)\$', r'\$\$(.*?)\$\$'
    ]
    
    return any(re.search(pattern, text) for pattern in math_indicators)

def is_numeric_expression(text):
    """Detecta si el texto es una expresión numérica (con o sin unidades)"""
    if not isinstance(text, str):
        return False
    
    # Patrones para detectar números con unidades
    numeric_patterns = [
        r'^\s*[-+]?\d*\.?\d+\s*(cm|mm|m|km|g|kg|°|grados|ºC|ºF)?\s*$',
        r'^\s*\d+\s*/\s*\d+\s*(cm|mm|m|km|g|kg|°|grados|ºC|ºF)?\s*$',
        r'^\s*\d+\.?\d*\s*(cm|mm|m|km|g|kg|°|grados|ºC|ºF)\s*$'
    ]
    
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in numeric_patterns)

def extract_math_content(text):
    """Extrae el contenido matemático de un texto"""
    if not isinstance(text, str):
        return ""
    
    patterns = [
        r'\\boxed\{([^}]*)\}',
        r'\$\$(.*?)\$\$',
        r'\$(.*?)\$',
        r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if content:
                return content
    
    return text.strip()

def latex_to_sympy(latex_str):
    """Convierte expresión LaTeX a SymPy"""
    try:
        if not latex_str or not isinstance(latex_str, str):
            return None
            
        # Limpiar espacios
        expr = latex_str.replace(' ', '').replace('\\ ', '')
        
        # Reemplazos de LaTeX a sintaxis SymPy
        replacements = [
            (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
            (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
            (r'\\cdot', '*'),
            (r'\\times', '*'),
            (r'\\left\(|\\right\)', ''),
            (r'\^\{([^}]+)\}', r'**(\1)'),
            (r'\^(\d+)', r'**\1'),
        ]
        
        for pattern, replacement in replacements:
            expr = re.sub(pattern, replacement, expr)
        
        # Definir variables comunes
        p, x, y, z, a, b, c = symbols('p x y z a b c')
        
        # Reemplazar variables
        variable_mapping = {
            'p': p, 'x': x, 'y': y, 'z': z, 
            'a': a, 'b': b, 'c': c
        }
        
        for var_name, var_symbol in variable_mapping.items():
            expr = re.sub(r'\b' + var_name + r'\b', f'symbols("{var_name}")', expr)
        
        return sp.sympify(expr)
    except:
        return None

def expressions_are_equivalent(expr1, expr2):
    """Determina si dos expresiones matemáticas son equivalentes"""
    try:
        sympy_expr1 = latex_to_sympy(expr1)
        sympy_expr2 = latex_to_sympy(expr2)
        
        if sympy_expr1 is None or sympy_expr2 is None:
            return False
        
        # Simplificar y comparar
        simplified1 = simplify(sympy_expr1)
        simplified2 = simplify(sympy_expr2)
        
        return simplify(simplified1 - simplified2) == 0
        
    except:
        return False

def normalize_numeric_expression(text):
    """Normaliza expresiones numéricas: quita unidades y convierte fracciones a decimales"""
    try:
        # Quitar unidades comunes
        units_pattern = r'\s*(cm|mm|m|km|g|kg|°|grados|ºC|ºF)\s*'
        clean_text = re.sub(units_pattern, '', text, flags=re.IGNORECASE).strip()
        
        # Verificar si es fracción (formato a/b)
        fraction_match = re.match(r'^\s*(\d+)\s*/\s*(\d+)\s*$', clean_text)
        if fraction_match:
            numerator = int(fraction_match.group(1))
            denominator = int(fraction_match.group(2))
            if denominator != 0:
                result = numerator / denominator
                # Redondear a 4 decimales para evitar floats largos
                return str(round(result, 4))
        
        # Verificar si ya es un número decimal
        try:
            # Intentar convertir directamente
            decimal_value = Decimal(clean_text)
            return str(float(decimal_value))  # Convertir a float y luego a string
        except (InvalidOperation, ValueError):
            # Si no es convertible directamente, intentar con sympy
            sympy_expr = latex_to_sympy(clean_text)
            if sympy_expr is not None:
                numeric_value = N(sympy_expr)  # Convertir a numérico
                return str(float(numeric_value))
            
        return clean_text
        
    except:
        return text

def normalize_math_expression(math_str):
    """Normaliza expresión matemática LaTeX: quita los $ y deja solo la fórmula"""
    try:
        # Primero extraer el contenido matemático (quita $$, $, \boxed, etc.)
        math_content = extract_math_content(math_str)
        
        # Si es una expresión que se puede simplificar, simplificarla
        sympy_expr = latex_to_sympy(math_content)
        if sympy_expr is not None:
            simplified = simplify(sympy_expr)
            # Convertir de vuelta a string (podrías implementar sympy_to_latex si necesitas)
            return str(simplified)
        
        return math_content  # Devolver solo la fórmula sin delimitadores
        
    except:
        return extract_math_content(math_str)

def normalize_text(text):
    """Normaliza texto general según los requisitos específicos"""
    if not isinstance(text, str):
        return ""
    
    # 1. Primero verificar si es expresión numérica (con unidades)
    if is_numeric_expression(text):
        return normalize_numeric_expression(text)
    
    # 2. Verificar si es expresión matemática LaTeX
    elif is_math_expression(text):
        return normalize_math_expression(text)
    
    # 3. Si no es ni numérica ni matemática, aplicar normalización de texto
    else:
        # Quitar delimitadores matemáticos si existen
        text = re.sub(r'\$\$|\$', '', text)
        text = re.sub(r'\\boxed{([^}]*)}', r'\1', text)
        text = re.sub(r'\\text{([^}]*)}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+', ' ', text)
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Normalizar caracteres Unicode
        nfkd_form = unicodedata.normalize('NFD', text)
        text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        # Quitar signos de puntuación y caracteres especiales, mantener números y letras
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # NUEVO: Quitar TODOS los espacios (no solo normalizar)
        text = re.sub(r'\s+', '', text).strip()
        
        return text

# Función adicional para clasificar y normalizar específicamente
def smart_normalize(text):
    """Función inteligente que clasifica y normaliza según el tipo de contenido"""
    if not isinstance(text, str):
        return {"tipo": "inválido", "normalizado": ""}
    
    # Detectar tipo de contenido
    if is_numeric_expression(text):
        return {"tipo": "numérico", "normalizado": normalize_numeric_expression(text)}
    elif is_math_expression(text):
        return {"tipo": "matemático", "normalizado": normalize_math_expression(text)}
    else:
        return {"tipo": "texto", "normalizado": normalize_text(text)}

# Ejemplos de prueba
if __name__ == "__main__":
    test_cases = [
        "Hola Mundo!",
        "5 cm",
        "1/2", 
        "$x^2 + 1$",
        "Texto con ESPACIOS  y signos!",
        "45°",
        "$$\frac{1}{2}$$"
    ]
    
    for test in test_cases:
        result = smart_normalize(test)
        print(f"Original: '{test}'")
        print(f"Tipo: {result['tipo']}")
        print(f"Normalizado: '{result['normalizado']}'")
        print("-" * 50)