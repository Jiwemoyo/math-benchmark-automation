
import pandas as pd
import sys
from .normalizer import normalize_text

def comparar_respuestas(csv_file, output_filename='resultados_comparados.csv'):
	try:
		df = pd.read_csv(csv_file)
		df['Respuesta'] = df['Respuesta'].fillna('')
		df['respuesta extraida'] = df['respuesta extraida'].fillna('')
		df['respuesta_normalizada'] = df['Respuesta'].apply(normalize_text)
		df['respuesta_extraida_normalizada'] = df['respuesta extraida'].apply(normalize_text)
		df['son_iguales'] = df['respuesta_normalizada'] == df['respuesta_extraida_normalizada']
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

