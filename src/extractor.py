import re
import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from .normalizer import to_inline_mode

# Cargar variables de entorno
load_dotenv()

# Configuración de IA
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
else:
    print("Advertencia: OPENAI_API_KEY no encontrada. El extractor no funcionará correctamente.")

# Instrucción para IA
INSTRUCCION_IA = """
Extrae SOLO la respuesta final del texto.

FORMATO DE SALIDA:
- Valor único: número, expresión LaTeX lineal, palabra o secuencia
- Múltiples valores: valor1 | valor2
- No claro: #Revision | Sin respuesta: ninguno | Infinito: infinito

REGLAS:
• Conserva TODOS los dígitos (ej: 0.0001 ✓, .0001 ✗)
• Elimina unidades
• Prioriza frases como 'la respuesta es', 'por lo tanto'
• Usa LaTeX lineal para matemáticas (ej: \sqrt{2}/2)

Ejemplos: 25.50, \pi/4, ABC123, #Revision 5 | estable, ninguno, infinito
"""

def extraer_respuesta(texto, numero_fila):
    """
    Función principal que extrae respuestas usando IA
    Mantiene la misma interfaz que el extractor original
    """
    if not texto or texto.isspace():
        print(f"--- Fila {numero_fila}: Celda vacía ---")
        return None
    
    if not client:
        print(f"!!! Error en Fila {numero_fila}: OPENAI_API_KEY no configurada")
        return "ERROR: API_KEY no configurada"
    
    print(f"--- Fila {numero_fila}: Procesando con IA ---")
    
    entrada = f"{INSTRUCCION_IA}\n\nTEXTO:\n{texto}"
    
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": entrada}],
            max_tokens=200,
            temperature=0.0
        )
        
        respuesta_ia = resp.choices[0].message.content.strip()
        print(f"Fila {numero_fila}: Respuesta extraída: '{respuesta_ia}'")
        
        # Pequeña pausa para no exceder límites de API
        time.sleep(1)
        
        return respuesta_ia

    except Exception as e:
        print(f"!!! Error en Fila {numero_fila}: {e}")
        return f"ERROR_API: {e}"