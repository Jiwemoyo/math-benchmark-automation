import pandas as pd
import sys
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de IA (igual que tu extractor)
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
else:
    print("Error: OPENAI_API_KEY no encontrada.")
    sys.exit(1)

# Instrucción para IA - Comparación de equivalencia
INSTRUCCION_COMPARACION = """
Eres un experto en evaluación matemática. Determina si estas dos respuestas son equivalentes en significado y valor matemático.

Responde EXCLUSIVAMENTE con una de estas opciones:

- "1" si las respuestas son equivalentes matemáticamente
- "0" si las respuestas no son equivalentes

CRITERIOS DE EQUIVALENCIA:
• Equivalencia numérica: 0.5 = 1/2 = 2/4 = 50%
• Simplificación algebraica: 2x + 2x = 4x
• Diferentes representaciones: π = 3.1416... (aproximaciones equivalentes)
• Unidades equivalentes: 1m = 100cm (si se especifican unidades)
• Pares y tuplas: (5, 10) = 5 y 10 = 5 | 10 = 5, 10
• Formato diferente pero mismo significado

Ejemplos que deben ser 1:
- "25" y "25.0"
- "1/2" y "0.5" 
- "x=5" y "5"
- "√4" y "2"
- "50%" y "0.5"

Ejemplos que deben ser 0:
- "10" y "11"
- "1/2" y "1/3"
- "x=5" y "x=6"

No des explicaciones, solo responde 1 o 0.
"""

def comparar_con_api(answer1, answer2, max_retries=3):
    """
    Compara dos respuestas usando solo la API de OpenAI
    Devuelve 1 si son equivalentes, 0 si no lo son
    """
    # Manejar casos vacíos directamente
    if not answer1 and not answer2:
        return 1
    if not answer1 or not answer2:
        return 0
    
    str1 = str(answer1).strip()
    str2 = str(answer2).strip()
    
    # Si son exactamente iguales, devolver 1 sin usar API
    if str1 == str2:
        return 1
    
    prompt = f"""
RESPUESTA 1: {str1}
RESPUESTA 2: {str2}

¿Son estas respuestas equivalentes matemáticamente? Responde solo con 1 o 0:
"""
    
    for attempt in range(max_retries):
        try:
            respuesta = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": INSTRUCCION_COMPARACION},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=5,
                temperature=0.0
            )
            
            contenido = respuesta.choices[0].message.content.strip()
            
            # Validar respuesta directamente como número
            if contenido == "1":
                return 1
            elif contenido == "0":
                return 0
            else:
                # Si la respuesta no es 1 o 0, intentar interpretar
                contenido_upper = contenido.upper()
                if any(palabra in contenido_upper for palabra in ["SÍ", "SI", "YES", "VERDADERO", "TRUE"]):
                    return 1
                elif any(palabra in contenido_upper for palabra in ["NO", "FALSE"]):
                    return 0
                else:
                    print(f"Respuesta no válida de API: '{contenido}', reintentando...")
                    continue
                
        except Exception as e:
            print(f"Error en API call (intento {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            continue
    
    # Si fallan todos los intentos, devolver 0 (no equivalentes)
    print(f"Falló API después de {max_retries} intentos, devolviendo 0")
    return 0

def comparar_respuestas(csv_file, output_filename='resultados_comparados.csv'):
    try:
        df = pd.read_csv(csv_file)
        df['Respuesta'] = df['Respuesta'].fillna('')
        df['respuesta extraida'] = df['respuesta extraida'].fillna('')
        
        print("=== COMPARADOR DE RESPUESTAS (SOLO API) ===")
        print(f"Archivo: {csv_file}")
        print(f"Filas a procesar: {len(df)}")
        print("-" * 50)
        
        resultados = []
        
        for idx, row in df.iterrows():
            respuesta1 = str(row['Respuesta']).strip()
            respuesta2 = str(row['respuesta extraida']).strip()
            
            # Siempre usar API para la comparación
            resultado = comparar_con_api(respuesta1, respuesta2)
            resultados.append(resultado)
            
            # Log de progreso
            print(f"Fila {idx+1}: {respuesta1} | {respuesta2} -> {resultado}")
            
            # Pausa para no exceder límites de API (igual que tu extractor)
            if (idx + 1) % 5 == 0:
                time.sleep(1)
        
        df['son_iguales'] = resultados
        
        print("\n" + "="*60)
        print("=== RESUMEN FINAL ===")
        conteo_iguales = df['son_iguales'].sum()
        total_filas = len(df)
        precision = (conteo_iguales / total_filas) * 100 if total_filas > 0 else 0
        
        print(f"Total de filas analizadas: {total_filas}")
        print(f"Respuestas equivalentes (1): {conteo_iguales}")
        print(f"Respuestas diferentes (0): {total_filas - conteo_iguales}")
        print(f"Tasa de equivalencia: {precision:.2f}%")
        
        if output_filename:
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"\nResultados guardados en: '{output_filename}'")
        
        return df
        
    except FileNotFoundError:
        print(f"Error: El archivo '{csv_file}' no se encontró.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

if __name__ == "__main__":
    # Permite ejecutar: python src/compare.py [archivo_entrada] [archivo_salida]
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'resultados.csv'
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'resultados_comparados.csv'
    
    comparar_respuestas(csv_file, output_filename)