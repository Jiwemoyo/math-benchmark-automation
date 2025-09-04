# Math Benchmark Automation

Este proyecto contiene scripts para la extracción y procesamiento de datos matemáticos. Por el momento, el único archivo funcional es `number_extraction.py`.

## Proceso de descarga y preparación

1. **Descarga el repositorio**
	 - Puedes descargar el proyecto como archivo ZIP desde GitHub o clonarlo usando:
		 ```powershell
		 git clone <URL_DEL_REPOSITORIO>
		 ```
	 - Entra a la carpeta del proyecto:
		 ```powershell
		 cd math-benchmark-automation
		 ```

2. **Crea un entorno virtual (recomendado)**
	 - En Windows (PowerShell):
		 ```powershell
		 python -m venv venv
		 .\venv\Scripts\Activate.ps1
		 ```
	 - En Linux/MacOS:
		 ```bash
		 python3 -m venv venv
		 source venv/bin/activate
		 ```

3. **Instala las dependencias**
	 - Ejecuta:
		 ```powershell
		 pip install -r requirements.txt
		 ```

## ¿Cómo probar el script?

1. Abre el archivo `number_extraction.py` en tu editor de texto o IDE favorito.
2. Localiza la variable llamada `texto_ejemplo_11` dentro del archivo.
3. Copia y pega el texto que deseas procesar dentro de esa variable, reemplazando el contenido de ejemplo si lo deseas.
4. Ejecuta el script manualmente para ver los resultados:
	 ```powershell
	 python number_extraction.py
	 ```

**Nota:** Actualmente no hay una interfaz de usuario ni entrada/salida automatizada. Todo el procesamiento se realiza modificando directamente el código fuente.

---

