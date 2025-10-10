import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import threading
import tempfile
from .csv_utils import procesar_csv
from .compare import comparar_respuestas


def run_gui():
    def seleccionar_entrada():
        archivo = filedialog.askopenfilename(
            title="Selecciona el archivo CSV de entrada",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if archivo:
            entrada_var.set(archivo)
            actualizar_estado_boton()

    def seleccionar_comparado():
        archivo = filedialog.asksaveasfilename(
            title="Selecciona dónde guardar el archivo FINAL de comparación",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if archivo:
            comparado_var.set(archivo)
            actualizar_estado_boton()

    def actualizar_estado_boton():
        # Habilita el botón solo si ambos archivos están seleccionados
        if entrada_var.get() and comparado_var.get():
            iniciar_btn.config(state="normal", bg="#27ae60", cursor="hand2")
        else:
            iniciar_btn.config(state="disabled", bg="#95a5a6", cursor="arrow")

    def validar_indices():
        try:
            idx_id = int(idx_id_var.get())
            idx_respuesta = int(idx_respuesta_var.get())
            idx_ia = int(idx_ia_var.get())
            return idx_id, idx_respuesta, idx_ia
        except ValueError:
            messagebox.showerror(
                "Error de validación", 
                "Los índices de columna deben ser números enteros válidos."
            )
            return None

    def ejecutar_proceso():
        # Validar archivos
        archivo_entrada = entrada_var.get()
        archivo_comparado = comparado_var.get()
        
        if not archivo_entrada or not archivo_comparado:
            messagebox.showerror(
                "Error", 
                "Debes seleccionar tanto el archivo de entrada como el archivo final."
            )
            return
            
        if not os.path.isfile(archivo_entrada):
            messagebox.showerror(
                "Error", 
                f"El archivo de entrada no existe:\n{archivo_entrada}"
            )
            return
            
        # Validar índices
        indices = validar_indices()
        if indices is None:
            return
            
        idx_id, idx_respuesta, idx_ia = indices
        
        # Deshabilitar interfaz durante el procesamiento
        toggle_interfaz(False)
        
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        
        # Ejecutar en hilo separado
        threading.Thread(
            target=procesar_con_barra, 
            args=(archivo_entrada, temp_file.name, idx_id, idx_respuesta, idx_ia, archivo_comparado, temp_file),
            daemon=True
        ).start()

    def procesar_con_barra(archivo_entrada, archivo_temp, idx_id, idx_respuesta, idx_ia, archivo_comparado, temp_file):
        try:
            # Procesar CSV
            procesar_csv(archivo_entrada, archivo_temp, idx_id, idx_respuesta, idx_ia)
            
            # Comparar respuestas
            comparar_respuestas(archivo_temp, output_filename=archivo_comparado)
            
            # Mostrar mensaje de éxito
            root.after(0, lambda: messagebox.showinfo(
                "Proceso completado", 
                f"¡El archivo final ha sido guardado en:\n{archivo_comparado}"
            ))
            
        except Exception as e:
            # Mostrar error
            root.after(0, lambda: messagebox.showerror(
                "Error al procesar", 
                f"Ocurrió un error durante el procesamiento:\n{str(e)}"
            ))
            
        finally:
            # Limpiar y restaurar interfaz
            root.after(0, lambda: finalizar_proceso(temp_file))

    def finalizar_proceso(temp_file):
        progress_bar.stop()
        progress_frame.pack_forget()
        toggle_interfaz(True)
        
        # Limpiar archivo temporal
        try:
            temp_file.close()
            os.remove(temp_file.name)
        except Exception:
            pass  # Ignorar errores al limpiar archivo temporal

    def toggle_interfaz(habilitar):
        estado = "normal" if habilitar else "disabled"
        entrada_btn.config(state=estado)
        comparado_btn.config(state=estado)
        iniciar_btn.config(state=estado)
        idx_id_entry.config(state=estado)
        idx_respuesta_entry.config(state=estado)
        idx_ia_entry.config(state=estado)
        
        if not habilitar:
            progress_frame.pack(pady=10, fill="x", padx=50)
            progress_bar.start(10)

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Automatización Benchmark Matemático")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Aplicar tema moderno
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configurar colores
    color_primario = "#2c3e50"
    color_secundario = "#3498db"
    color_exito = "#27ae60"
    color_deshabilitado = "#95a5a6"
    
    root.configure(bg='white')
    
    # Título principal
    titulo = tk.Label(
        root, 
        text="Automatización Benchmark Matemático", 
        font=("Arial", 16, "bold"),
        bg='white',
        fg=color_primario
    )
    titulo.pack(pady=20)
    
    # Frame principal para contenido
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill="both", expand=True, padx=30)
    
    # Sección de archivo de entrada
    entrada_frame = tk.Frame(main_frame, bg='white')
    entrada_frame.pack(fill="x", pady=10)
    
    tk.Label(
        entrada_frame, 
        text="Archivo CSV de entrada:", 
        font=("Arial", 10, "bold"),
        bg='white',
        anchor="w"
    ).pack(fill="x")
    
    entrada_subframe = tk.Frame(entrada_frame, bg='white')
    entrada_subframe.pack(fill="x", pady=5)
    
    entrada_var = tk.StringVar()
    entrada_entry = tk.Entry(
        entrada_subframe, 
        textvariable=entrada_var, 
        width=50,
        font=("Arial", 9),
        state="readonly"
    )
    entrada_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    entrada_btn = tk.Button(
        entrada_subframe, 
        text="Examinar...", 
        command=seleccionar_entrada,
        bg=color_secundario,
        fg="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        padx=15,
        cursor="hand2"
    )
    entrada_btn.pack(side="right")
    
    # Sección de archivo de salida
    comparado_frame = tk.Frame(main_frame, bg='white')
    comparado_frame.pack(fill="x", pady=10)
    
    tk.Label(
        comparado_frame, 
        text="Ubicación de guardado del archivo de salida:", 
        font=("Arial", 10, "bold"),
        bg='white',
        anchor="w"
    ).pack(fill="x")
    
    comparado_subframe = tk.Frame(comparado_frame, bg='white')
    comparado_subframe.pack(fill="x", pady=5)
    
    comparado_var = tk.StringVar(value="resultados_comparados.csv")
    comparado_entry = tk.Entry(
        comparado_subframe, 
        textvariable=comparado_var, 
        width=50,
        font=("Arial", 9)
    )
    comparado_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    comparado_btn = tk.Button(
        comparado_subframe, 
        text="Examinar...", 
        command=seleccionar_comparado,
        bg=color_secundario,
        fg="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        padx=15,
        cursor="hand2"
    )
    comparado_btn.pack(side="right")
    
    # Sección de índices de columnas
    indices_frame = tk.Frame(main_frame, bg='white')
    indices_frame.pack(fill="x", pady=20)
    
    tk.Label(
        indices_frame, 
        text="Configuración de Columnas:", 
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(fill="x", pady=(0, 10))
    
    indices_subframe = tk.Frame(indices_frame, bg='white')
    indices_subframe.pack(fill="x")
    
    # Índice ID
    idx_id_var = tk.StringVar(value="0")
    tk.Label(
        indices_subframe, 
        text="Columna ID:", 
        bg='white',
        font=("Arial", 9)
    ).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
    
    idx_id_entry = tk.Entry(
        indices_subframe, 
        textvariable=idx_id_var, 
        width=8,
        font=("Arial", 9),
        justify="center"
    )
    idx_id_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(
        indices_subframe, 
        text="(ej. 0 para columna A)", 
        bg='white',
        font=("Arial", 8),
        fg="gray"
    ).grid(row=0, column=2, padx=(5, 20), pady=5, sticky="w")
    
    # Índice Respuesta
    idx_respuesta_var = tk.StringVar(value="4")
    tk.Label(
        indices_subframe, 
        text="Columna Respuesta Matematico:", 
        bg='white',
        font=("Arial", 9)
    ).grid(row=0, column=3, padx=(0, 5), pady=5, sticky="e")
    
    idx_respuesta_entry = tk.Entry(
        indices_subframe, 
        textvariable=idx_respuesta_var, 
        width=8,
        font=("Arial", 9),
        justify="center"
    )
    idx_respuesta_entry.grid(row=0, column=4, padx=5, pady=5)
    tk.Label(
        indices_subframe, 
        text="(ej. 4 para columna E)", 
        bg='white',
        font=("Arial", 8),
        fg="gray"
    ).grid(row=0, column=5, padx=5, pady=5, sticky="w")
    
    # Índice Extracción
    idx_ia_var = tk.StringVar(value="6")
    tk.Label(
        indices_subframe, 
        text="Columna Extracción:", 
        bg='white',
        font=("Arial", 9)
    ).grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
    
    idx_ia_entry = tk.Entry(
        indices_subframe, 
        textvariable=idx_ia_var, 
        width=8,
        font=("Arial", 9),
        justify="center"
    )
    idx_ia_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(
        indices_subframe, 
        text="(ej. 6 para columna G)", 
        bg='white',
        font=("Arial", 8),
        fg="gray"
    ).grid(row=1, column=2, padx=(5, 20), pady=5, sticky="w")
    
    # Botón de inicio
    boton_frame = tk.Frame(main_frame, bg='white')
    boton_frame.pack(fill="x", pady=30)
    
    iniciar_btn = tk.Button(
        boton_frame, 
        text="Iniciar Procesamiento", 
        command=ejecutar_proceso,
        bg=color_deshabilitado,
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        height=2,
        width=20,
        state="disabled",
        cursor="arrow"
    )
    iniciar_btn.pack()
    
    # Barra de progreso (inicialmente oculta)
    progress_frame = tk.Frame(main_frame, bg='white')
    
    progress_bar = ttk.Progressbar(
        progress_frame, 
        mode="indeterminate", 
        length=400
    )
    progress_bar.pack(pady=10)
    
    tk.Label(
        progress_frame, 
        text="Procesando archivos...", 
        bg='white',
        font=("Arial", 9),
        fg=color_primario
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    run_gui()