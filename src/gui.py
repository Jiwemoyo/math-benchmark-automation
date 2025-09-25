import tkinter as tk
from tkinter import filedialog, messagebox
import os
from .csv_utils import procesar_csv

def run_gui():
    def seleccionar_entrada():
        archivo = filedialog.askopenfilename(title="Selecciona el archivo CSV de entrada", filetypes=[("CSV files", "*.csv")])
        entrada_var.set(archivo)

    def seleccionar_salida():
        archivo = filedialog.asksaveasfilename(title="Selecciona dónde guardar el archivo CSV de salida", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        salida_var.set(archivo)

    def ejecutar_proceso():
        archivo_entrada = entrada_var.get()
        archivo_salida = salida_var.get()
        if not archivo_entrada or not archivo_salida:
            messagebox.showerror("Error", "Debes seleccionar ambos archivos.")
            return
        if not os.path.isfile(archivo_entrada):
            messagebox.showerror("Error", f"El archivo de entrada no existe: {archivo_entrada}")
            return
        try:
            procesar_csv(archivo_entrada, archivo_salida)
            messagebox.showinfo("Proceso completado", f"¡El proceso ha finalizado!\nArchivo guardado en: {archivo_salida}")
        except Exception as e:
            messagebox.showerror("Error al procesar", str(e))

    root = tk.Tk()
    root.title("Automatización Benchmark Matemático")
    root.geometry("500x250")

    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()

    tk.Label(root, text="Archivo CSV de entrada:").pack(pady=(20,0))
    tk.Entry(root, textvariable=entrada_var, width=50).pack(padx=10)
    tk.Button(root, text="Seleccionar archivo...", command=seleccionar_entrada).pack(pady=5)

    tk.Label(root, text="Archivo CSV de salida:").pack(pady=(10,0))
    tk.Entry(root, textvariable=salida_var, width=50).pack(padx=10)
    tk.Button(root, text="Seleccionar destino...", command=seleccionar_salida).pack(pady=5)

    tk.Button(root, text="Iniciar", command=ejecutar_proceso, bg="#4CAF50", fg="white", height=2, width=20).pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
