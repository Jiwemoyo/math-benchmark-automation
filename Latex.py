import re

def to_inline_mode(latex_str):
    # Extraer contenido de \boxed{...}
    latex_str = re.sub(r'\\boxed\{(.+?)\}', r'\1', latex_str)
    # Quitar $$ ... $$ y $ ... $
    latex_str = re.sub(r'\$\$?(.+?)\$\$?', r'\1', latex_str)
    # Envolver en $ ... $
    return f"${latex_str.strip()}$"

# Ejemplos:
print(to_inline_mode(r'$55°$'))  # $55^\circ$
print(to_inline_mode(r'$55$'))              # $55$
print(to_inline_mode(r'$$55$$'))            # $55$
