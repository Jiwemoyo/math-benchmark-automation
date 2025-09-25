import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from .csv_utils import procesar_csv
import threading
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
        archivo = filedialog.askopenfilename(title="Selecciona el archivo CSV de entrada", filetypes=[("CSV files", "*.csv")])
        entrada_var.set(archivo)

    def seleccionar_comparado():
        archivo = filedialog.asksaveasfilename(title="Selecciona dónde guardar el archivo FINAL de comparación", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        comparado_var.set(archivo)

    def ejecutar_proceso():
        archivo_entrada = entrada_var.get()
        archivo_comparado = comparado_var.get()
        try:
            idx_id = int(idx_id_var.get())
            idx_respuesta = int(idx_respuesta_var.get())
            idx_ia = int(idx_ia_var.get())
        except ValueError:
            messagebox.showerror("Error", "Los índices de columna deben ser números enteros.")
            return
        if not archivo_entrada or not archivo_comparado:
            messagebox.showerror("Error", "Debes seleccionar el archivo de entrada y el archivo final.")
            return
        if not os.path.isfile(archivo_entrada):
            messagebox.showerror("Error", f"El archivo de entrada no existe: {archivo_entrada}")
            return
        iniciar_btn.config(state="disabled")
        progress_bar.pack(pady=10)
        root.update_idletasks()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        threading.Thread(target=procesar_con_barra, args=(archivo_entrada, temp_file.name, idx_id, idx_respuesta, idx_ia, archivo_comparado, temp_file), daemon=True).start()

    def procesar_con_barra(archivo_entrada, archivo_temp, idx_id, idx_respuesta, idx_ia, archivo_comparado, temp_file):
        try:
            progress_bar.start(10)
            procesar_csv(archivo_entrada, archivo_temp, idx_id, idx_respuesta, idx_ia)
            comparar_respuestas(archivo_temp, output_filename=archivo_comparado)
        finally:
            progress_bar.stop()
            progress_bar.pack_forget()
            iniciar_btn.config(state="normal")
            temp_file.close()
            os.remove(temp_file.name)
        try:
            messagebox.showinfo("Proceso completado", f"¡El archivo final ha sido guardado en:\n{archivo_comparado}")
        except Exception as e:
            messagebox.showerror("Error al procesar", str(e))

    root = tk.Tk()
    root.title("Automatización Benchmark Matemático")
    root.geometry("500x300")

    entrada_var = tk.StringVar()
    comparado_var = tk.StringVar(value="resultados_comparados.csv")
    idx_id_var = tk.StringVar(value="0")
    idx_respuesta_var = tk.StringVar(value="4")
    idx_ia_var = tk.StringVar(value="6")

    tk.Label(root, text="Archivo CSV de entrada:").pack(pady=(20,0))
    tk.Entry(root, textvariable=entrada_var, width=50).pack(padx=10)
    tk.Button(root, text="Seleccionar archivo...", command=seleccionar_entrada).pack(pady=5)

    tk.Label(root, text="Archivo FINAL de comparación:").pack(pady=(10,0))
    tk.Entry(root, textvariable=comparado_var, width=50).pack(padx=10)
    tk.Button(root, text="Seleccionar destino final...", command=seleccionar_comparado).pack(pady=5)

    frame_indices = tk.Frame(root)
    frame_indices.pack(pady=(10,0))
    tk.Label(frame_indices, text="Columna ID (ej. 0 para A):").grid(row=0, column=0, padx=5)
    tk.Entry(frame_indices, textvariable=idx_id_var, width=5).grid(row=0, column=1, padx=5)
    tk.Label(frame_indices, text="Columna Respuesta (ej. 4 para E):").grid(row=0, column=2, padx=5)
    tk.Entry(frame_indices, textvariable=idx_respuesta_var, width=5).grid(row=0, column=3, padx=5)
    tk.Label(frame_indices, text="Columna IA (ej. 6 para G):").grid(row=0, column=4, padx=5)
    tk.Entry(frame_indices, textvariable=idx_ia_var, width=5).grid(row=0, column=5, padx=5)

    iniciar_btn = tk.Button(root, text="Iniciar", command=ejecutar_proceso, bg="#4CAF50", fg="white", height=2, width=20)
    iniciar_btn.pack(pady=15)
    progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
