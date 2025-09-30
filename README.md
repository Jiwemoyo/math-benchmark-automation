# Math Benchmark Automation

Automatiza la extracción y comparación de respuestas matemáticas en archivos CSV usando IA (OpenAI) y una interfaz gráfica amigable.

## Características
- Extracción automática de respuestas finales desde textos usando IA (GPT-4o).
- Comparación inteligente de respuestas (soporta equivalencia matemática y textual).
- Soporte para prompts en español e inglés (seleccionable en la GUI).
- Interfaz gráfica (Tkinter) para seleccionar archivos, columnas y opciones.
- Resultados exportados a un nuevo archivo CSV.

## Requisitos
- Python 3.10+
- Dependencias del archivo `requirements.txt`
- Una clave de API de OpenAI (variable de entorno `OPENAI_API_KEY`)

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/math-benchmark-automation.git
   cd math-benchmark-automation
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` en la raíz del proyecto con tu clave de OpenAI:
   ```env
   OPENAI_API_KEY=sk-...tu_clave...
   ```

## Uso
1. Ejecuta la interfaz gráfica:
   ```bash
   python -m src.gui
   ```
2. En la ventana:
   - Selecciona el archivo CSV de entrada.
   - Selecciona el archivo de salida.
   - Indica los índices de columna para ID, Respuesta y Texto IA.
   - Elige el idioma del prompt (español o inglés).
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
- El selector de idioma afecta tanto la extracción como la comparación.

## Licencia
MIT# Math Benchmark Automation

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

