import tkinter as tk
import subprocess
import sys
import os
from tkinter import messagebox


class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Generadores Pseudoaleatorios")
        self.root.geometry("500x300")
        self.root.configure(bg="#f5f5f5")

        # Título
        tk.Label(root, text="Seleccione un método de generación",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=20)

        # Botones
        btn1 = tk.Button(root,
                         text="Algoritmo de cuadrados medios (1 semilla)",
                         command=lambda: self.abrir_modulo("cuadradosMedios.py"),
                         font=("Arial", 12),
                         width=40,
                         bg="#007bff", fg="white")
        btn1.pack(pady=10)

        btn2 = tk.Button(root,
                         text="Algoritmo de productos medios (2 semillas)",
                         command=lambda: self.abrir_modulo("productosMedios.py"),
                         font=("Arial", 12),
                         width=40,
                         bg="#28a745", fg="white")
        btn2.pack(pady=10)

        btn3 = tk.Button(root,
                         text="Algoritmo multiplicador constante",
                         command=lambda: self.abrir_modulo("multiplicadorConst.py"),
                         font=("Arial", 12),
                         width=40,
                         bg="#ffc107", fg="black")
        btn3.pack(pady=10)

        tk.Label(root, text="Adriet Daniela Chuquimia Centeno",
             font=("Arial", 8, "bold"), bg="#f5f5f5").pack(pady=20)

    def abrir_modulo(self, archivo):
        """Ejecuta otro script Python y cierra la ventana actual."""
        ruta = os.path.join(os.path.dirname(__file__), archivo)
        if os.path.exists(ruta):
            self.root.destroy()  # 🔹 Cierra la ventana actual
            subprocess.Popen([sys.executable, ruta])
        else:
            messagebox.showerror("Error", f"No se encontró el archivo: {archivo}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
