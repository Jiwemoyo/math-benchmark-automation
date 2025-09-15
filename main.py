from src.csv_utils import procesar_csv
import subprocess
import sys

if __name__ == "__main__":
    archivo_csv_entrada = "datos.csv"
    archivo_csv_salida = "resultados.csv"
    procesar_csv(archivo_csv_entrada, archivo_csv_salida)

    # Ejecutar src.compare como módulo automaticamente al finalizar
    subprocess.run([sys.executable, "-m", "src.compare", archivo_csv_salida])