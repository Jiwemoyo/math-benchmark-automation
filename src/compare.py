import pandas as pd
import sys
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de IA
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
else:
    print("Error: OPENAI_API_KEY no encontrada.")
    sys.exit(1)

# Instrucción mantenida pero con formato más eficiente
INSTRUCCION_COMPARACION = """Evalúa si las respuestas son equivalentes en significado, valor textual o matemático (ignora unidades). Responde SOLO con 1 (equivalentes) o 0 (no equivalentes)."""

def comparar_con_api(answer1, answer2, max_retries=2):
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
    
    # PROMPT EFICIENTE pero manteniendo la versatilidad
    prompt = f"""R1: {str1}
R2: {str2}
¿Equivalentes? [1/0]:"""
    
    for attempt in range(max_retries):
        try:
            respuesta = client.chat.completions.create(
                model="gpt-4o",  # Modelo más económico
                messages=[
                    {"role": "system", "content": INSTRUCCION_COMPARACION},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3,  # Solo necesita 1 token pero por seguridad 3
                temperature=0.0
            )
            
            contenido = respuesta.choices[0].message.content.strip()
            
            # Validación robusta pero simple
            if any(indicator in contenido for indicator in ["1", "sí", "si", "yes", "true"]):
                return 1
            elif any(indicator in contenido for indicator in ["0", "no", "false"]):
                return 0
            else:
                # Si la respuesta no es clara, considerar como no equivalentes
                return 0
                
        except Exception as e:
            print(f"Error en API call (intento {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            continue
    
    return 0

def comparar_respuestas(csv_file, output_filename='resultados_comparados.csv'):
    try:
        df = pd.read_csv(csv_file)
        print("=== COMPARADOR DE RESPUESTAS (OPTIMIZADO) ===")
        print(f"Archivo: {csv_file}")
        print(f"Columnas: {df.columns.tolist()}")
        print(f"Filas a procesar: {len(df)}")
        print("-" * 50)

        # Detección automática de columnas
        columnas = df.columns.tolist()
        
        idx_extraida = None
        for i, col in enumerate(columnas):
            if 'extraida' in col.lower() or 'extraída' in col.lower():
                idx_extraida = i
                break
        
        if idx_extraida is None:
            idx_extraida = len(columnas) - 1
            print(f"Usando última columna como respuesta extraída: {columnas[idx_extraida]}")
        
        idx_respuesta = 1
        
        print(f"Comparando: '{columnas[idx_respuesta]}' vs '{columnas[idx_extraida]}'")
        print("-" * 50)
        
        resultados = []
        llamadas_api = 0
        ahorros = 0

        for idx, row in df.iterrows():
            try:
                respuesta_matematico = str(row[columnas[idx_respuesta]]).strip()
                respuesta_extraida = str(row[columnas[idx_extraida]]).strip()
            except Exception as e:
                print(f"Error accediendo a columnas en fila {idx+1}: {e}")
                respuesta_matematico = ""
                respuesta_extraida = ""

            # Verificaciones previas para evitar llamadas a API
            if not respuesta_matematico and not respuesta_extraida:
                resultado = 1
                ahorros += 1
            elif respuesta_matematico == respuesta_extraida:
                resultado = 1
                ahorros += 1
            else:
                resultado = comparar_con_api(respuesta_matematico, respuesta_extraida)
                llamadas_api += 1

            resultados.append(resultado)

            # Log informativo pero eficiente
            print(f"Fila {idx+1}: {resultado}")
            print(f"  Matemático: {respuesta_matematico[:80]}{'...' if len(respuesta_matematico) > 80 else ''}")
            print(f"  Extraída:   {respuesta_extraida[:80]}{'...' if len(respuesta_extraida) > 80 else ''}")
            print("-" * 40)

            if (idx + 1) % 3 == 0:  # Pausa ligera cada 3 filas
                time.sleep(0.5)

        df['son_iguales'] = resultados

        print("\n" + "="*60)
        print("=== RESUMEN OPTIMIZADO ===")
        conteo_iguales = df['son_iguales'].sum()
        total_filas = len(df)
        precision = (conteo_iguales / total_filas) * 100 if total_filas > 0 else 0

        print(f"Total de filas analizadas: {total_filas}")
        print(f"Llamadas a API realizadas: {llamadas_api}")
        print(f"Llamadas a API evitadas: {ahorros}")
        print(f"Respuestas equivalentes (1): {conteo_iguales}")
        print(f"Respuestas diferentes (0): {total_filas - conteo_iguales}")
        print(f"Tasa de equivalencia: {precision:.2f}%")
        print(f"Eficiencia: {(ahorros/total_filas)*100:.1f}% de ahorro en llamadas")

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
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'resultados.csv'
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'resultados_comparados.csv'
    
    comparar_respuestas(csv_file, output_filename)