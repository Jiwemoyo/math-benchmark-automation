import re
import unicodedata
import sympy as sp
from sympy import simplify, symbols

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

def normalize_math_expression(math_str):
    """Normaliza expresión matemática para visualización"""
    try:
        sympy_expr = latex_to_sympy(math_str)
        if sympy_expr is not None:
            return str(simplify(sympy_expr))
    except:
        pass
    return math_str

def normalize_text(text):
    """Normaliza texto general (no matemático) - TU FUNCIÓN ORIGINAL MEJORADA"""
    if not isinstance(text, str):
        return ""
    
    # Primero verificar si es expresión matemática
    if is_math_expression(text):
        math_content = extract_math_content(text)
        normalized_math = normalize_math_expression(math_content)
        return normalized_math
    
    # Si no es matemática, aplicar normalización original
    text = re.sub(r'\$\$|\$', '', text)
    text = re.sub(r'\\boxed{([^}]*)}', r'\1', text)
    text = re.sub(r'\\text{([^}]*)}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', ' ', text)
    text = text.lower()
    nfkd_form = unicodedata.normalize('NFD', text)
    text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text