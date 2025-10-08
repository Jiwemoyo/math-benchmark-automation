

# Math Benchmark Automation

Automatiza la extracción y comparación de respuestas matemáticas en archivos CSV usando IA (OpenAI) y una interfaz gráfica sencilla.

## Características
- Extracción automática de respuestas finales desde textos usando IA (GPT-4o).
- Comparación inteligente de respuestas (soporta equivalencia matemática y textual).
- Interfaz gráfica (Tkinter) para seleccionar archivos, columnas y opciones.
- Resultados exportados a un nuevo archivo CSV.

## Requisitos
- Python 3.10+
- Dependencias del archivo `requirements.txt`
- Una clave de API de OpenAI (variable de entorno `OPENAI_API_KEY`)



## Guía rápida para usuarios 

### 1. Descarga el proyecto
Puedes descargar el proyecto como archivo ZIP desde GitHub (botón "Code" > "Download ZIP") o, si tienes Git instalado, puedes usar este comando en PowerShell:

```powershell
git clone <URL_DEL_REPOSITORIO>
cd math-benchmark-automation
```

### 2. Instala Python
Asegúrate de tener Python 3.10 o superior instalado. Puedes descargarlo desde https://www.python.org/downloads/

### 3. Crea un entorno virtual (opcional pero recomendado)
En PowerShell, ejecuta:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Instala las dependencias
Con el entorno virtual activado, ejecuta:

```powershell
pip install -r requirements.txt
```

### 5. Configura tu clave de OpenAI
Crea un archivo llamado `.env` en la carpeta principal del proyecto y pega tu clave de OpenAI así:

```env
OPENAI_API_KEY=sk-...tu_clave...
```

### 6. Ejecuta la interfaz gráfica
En la misma carpeta, ejecuta este comando:

```powershell
python -m src.gui
```

Se abrirá una ventana donde podrás seleccionar tu archivo CSV de entrada, el archivo de salida y los índices de columna. Haz clic en "Iniciar" y espera el resultado.

---

## ¿Cómo usar la interfaz gráfica?

1. Selecciona el archivo CSV de entrada (el archivo con los datos que quieres analizar).
2. Selecciona el archivo de salida (donde se guardarán los resultados).
3. Indica los índices de columna para:
	- ID (por ejemplo, columna 0)
	- Respuesta (por ejemplo, columna 4)
	- Texto IA (por ejemplo, columna 6)
	Si no sabes los índices, abre tu archivo CSV en Excel y cuenta desde la columna A=0, B=1, C=2, etc.
4. Haz clic en "Iniciar" y espera a que el proceso termine.
5. El archivo de salida tendrá los resultados y una columna de revisión si alguna respuesta es ambigua.

## ¿Cómo debe estar tu archivo CSV?
El archivo debe tener al menos estas columnas:
- ID (ejemplo: columna 0)
- Respuesta (ejemplo: columna 4)
- Texto IA (ejemplo: columna 6)
Puedes ajustar los índices según tu archivo. Si tienes dudas, abre el archivo en Excel y verifica el orden de las columnas.

## Notas importantes
- El procesamiento usa la API de OpenAI, asegúrate de tener saldo y acceso a GPT-4o.
- El resultado se guarda en el archivo de salida que elijas, con una columna adicional de comparación 

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


