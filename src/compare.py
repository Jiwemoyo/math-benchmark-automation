import pandas as pd
import sys
from .normalizer import normalize_text, is_math_expression, extract_math_content, expressions_are_equivalent

def compare_answers(answer1, answer2):
    """Compara dos respuestas usando el método apropiado"""
    # Manejar valores nulos o vacíos
    if not answer1 and not answer2:
        return True
    if not answer1 or not answer2:
        return False
    
    str1 = str(answer1).strip()
    str2 = str(answer2).strip()
    
    # Detectar si son expresiones matemáticas
    is_math1 = is_math_expression(str1)
    is_math2 = is_math_expression(str2)
    
    # Si ambas son matemáticas, usar comparación algebraica
    if is_math1 and is_math2:
        math_expr1 = extract_math_content(str1)
        math_expr2 = extract_math_content(str2)
        return expressions_are_equivalent(math_expr1, math_expr2)
    
    # Si una es matemática y la otra no, o ambas son texto, usar normalización de texto
    norm1 = normalize_text(str1)
    norm2 = normalize_text(str2)
    return norm1 == norm2

def comparar_respuestas(csv_file, output_filename='resultados_comparados.csv'):
    try:
        df = pd.read_csv(csv_file)
        df['Respuesta'] = df['Respuesta'].fillna('')
        df['respuesta extraida'] = df['respuesta extraida'].fillna('')
        
        # Usar comparación inteligente y convertir True/False a 1/0
        df['son_iguales'] = df.apply(
            lambda row: 1 if compare_answers(row['Respuesta'], row['respuesta extraida']) else 0,
            axis=1
        )
        
        # Normalizar para visualización (usando la misma función normalize_text)
        df['respuesta_normalizada'] = df['Respuesta'].apply(normalize_text)
        df['respuesta_extraida_normalizada'] = df['respuesta extraida'].apply(normalize_text)
        
        print("--- Tabla de Comparación de Respuestas ---")
        print(df[[
            'ID',
            'son_iguales',
            'respuesta_normalizada',
            'respuesta_extraida_normalizada'
        ]].to_string())
        
        print("\n" + "="*50 + "\n")
        print("--- Resumen de la Comparación ---")
        conteo_iguales = df['son_iguales'].sum()
        total_filas = len(df)
        diferencias = total_filas - conteo_iguales
        print(f"Total de filas analizadas: {total_filas}")
        print(f"Respuestas coincidentes (después de normalizar): {conteo_iguales}")
        print(f"Respuestas diferentes: {diferencias}")
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"\nResultados guardados en el archivo '{output_filename}'")
        
    except FileNotFoundError:
        print(f"Error: El archivo '{csv_file}' no se encontró.")
        print("Por favor, asegúrate de que el script se está ejecutando en la misma carpeta que tu archivo CSV.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Permite ejecutar: python src/compare.py [archivo_entrada] [archivo_salida]
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'resultados.csv'
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'resultados_comparados.csv'
    comparar_respuestas(csv_file, output_filename)