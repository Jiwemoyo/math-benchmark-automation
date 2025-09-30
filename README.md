
# Math Benchmark Automation

Automatiza la extracción y comparación de respuestas matemáticas en archivos CSV usando IA (OpenAI) y una interfaz gráfica amigable.

## Características
- Extracción automática de respuestas finales desde textos usando IA (GPT-4o).
- Comparación inteligente de respuestas (soporta equivalencia matemática y textual).
- Interfaz gráfica (Tkinter) para seleccionar archivos, columnas y opciones.
- Resultados exportados a un nuevo archivo CSV.

## Requisitos
- Python 3.10+
- Dependencias del archivo `requirements.txt`
- Una clave de API de OpenAI (variable de entorno `OPENAI_API_KEY`)


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

4. **Crea el archivo de configuración**
	 - Crea un archivo `.env` en la raíz del proyecto con tu clave de OpenAI:
		 ```env
		 OPENAI_API_KEY=sk-...tu_clave...
		 ```

## Cómo ejecutar
1. Ejecuta la interfaz gráfica:
   ```bash
   python -m src.gui
   ```
2. En la ventana:
	- Selecciona el archivo CSV de entrada.
	- Selecciona el archivo de salida.
	- Indica los índices de columna para ID, Respuesta y Texto IA.
	- Haz clic en "Iniciar" y espera el resultado.

## Estructura esperada del CSV
El archivo de entrada debe tener al menos las siguientes columnas:
- ID (ejemplo: columna 0)
- Respuesta (ejemplo: columna 4)
- Texto IA (ejemplo: columna 6)

Puedes ajustar los índices según tu archivo.

## Notas
- El procesamiento usa la API de OpenAI, asegúrate de tener saldo y acceso a GPT-4o.
- El resultado se guarda en el archivo de salida que elijas, con una columna adicional de comparación.

## Licencia
MIT

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


