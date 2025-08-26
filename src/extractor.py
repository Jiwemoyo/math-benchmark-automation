import re

def extraer_respuesta(texto):
    """
    Extrae la respuesta matemática del texto usando patrones regex
    """
    if not texto or not isinstance(texto, str):
        return None
    
    patrones = [
        r'\\boxed\{([^}]+)\}',                      # \boxed{respuesta}
        r'Respuesta[:\s]*([^\n]+)',                 # Respuesta: valor
        r'respuesta[:\s]*([^\n]+)',                 # respuesta: valor (minúscula)
        r'\\boxed\{([^}]+)\}',                      # formato LaTeX
        r'(\d+\.?\d*)\s*(?:cm|kg|°|grados|unidades)?',  # valores numéricos
        r'\\frac\{([^}]+)\}\{([^}]+)\}',            # fracciones LaTeX
        r'(\w+)\s*=\s*([^\n]+)',                    # variable = valor
    ]
    
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        if matches:
            # Para fracciones, combinamos numerador y denominador
            if patron == r'\\frac\{([^}]+)\}\{([^}]+)\}':
                for match in matches:
                    if len(match) == 2:
                        return f"{match[0]}/{match[1]}"
            # Para otros patrones
            else:
                return matches[0] if isinstance(matches[0], str) else str(matches[0])
    
    return None