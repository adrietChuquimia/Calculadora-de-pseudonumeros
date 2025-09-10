import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pypandoc
from scipy.stats import chi2, norm
import os
import subprocess
import sys

class GeneradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Pseudoaleatorio - Multiplicador Constante")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        self.numeros = []
        self.iteraciones = []

        # --- Entradas ---
        frame = tk.Frame(root, bg="#f5f5f5")
        frame.pack(pady=10)

        tk.Label(frame, text="Cantidad de números:", bg="#f5f5f5").grid(row=0, column=0, sticky="w")
        self.cantidad_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.cantidad_var, width=10).grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Semilla 1 (min. 4 dígitos):", bg="#f5f5f5").grid(row=1, column=0, sticky="w")
        self.semilla1_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.semilla1_var, width=15).grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Multiplicador (min. 4 dígitos):", bg="#f5f5f5").grid(row=2, column=0, sticky="w")
        self.semilla2_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.semilla2_var, width=15).grid(row=2, column=1, padx=5)

        tk.Label(frame, text="Nivel de confianza (ej. 0.05):", bg="#f5f5f5").grid(row=3, column=0, sticky="w")
        self.alpha_var = tk.StringVar(value="0.05")
        tk.Entry(frame, textvariable=self.alpha_var, width=10).grid(row=3, column=1, padx=5)

        # --- Botones ---
        botones = tk.Frame(root, bg="#f5f5f5")
        botones.pack(pady=10)
        ttk.Button(botones, text="Generar", command=self.generar).grid(row=0, column=0, padx=10)
        ttk.Button(botones, text="Mostrar estadísticas", command=self.estadisticas).grid(row=0, column=1, padx=10)
        ttk.Button(botones, text="Exportar", command=self.exportar).grid(row=0, column=2, padx=10)
        ttk.Button(botones, text="Mostrar histogramas", command=self.histogramas).grid(row=0, column=3, padx=10)
        ttk.Button(botones, text="Regresar al menú", command=lambda: self.abrir_modulo("main.py")).grid(row=0, column=4, padx=10)
        # --- Tabla de iteraciones ---
        self.tree = ttk.Treeview(root, columns=("Iter", "Producto", "Centro", "Número"), show="headings", height=15)
        self.tree.heading("Iter", text="Iteración")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Centro", text="Centro")
        self.tree.heading("Número", text="Número generado")
        self.tree.pack(pady=10, fill="both", expand=True)

    def generar(self):
        try:
            cantidad = int(self.cantidad_var.get())
            x0 = self.semilla1_var.get()
            A = self.semilla2_var.get()

            if not (x0.isdigit() and A.isdigit() and len(x0) >= 4 and len(A) >= 4):
                messagebox.showerror("Error", "La semilla y multiplicador deben ser numéricas y tener al menos 4 dígitos.")
                return

            x0, A = int(x0), int(A)
            n = max(len(str(x0)), len(str(A)))
            self.numeros = []
            self.iteraciones = []

            # limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            for i in range(cantidad):
                producto = x0 * A
                prod_str = str(producto)

                if len(prod_str) % 2 != 0:
                    prod_str = "0" + prod_str

                inicio = (len(prod_str) - n) // 2
                centro = prod_str[inicio: inicio + n]

                numero_final = int(centro) / (10 ** n)
                self.numeros.append(numero_final)
                self.iteraciones.append((i+1, prod_str, centro, numero_final))

                self.tree.insert("", "end", values=(i+1, prod_str, centro, f"{numero_final:.4f}"))

                x0 = int(centro)

            messagebox.showinfo("Éxito", f"Se generaron {len(self.numeros)} números.")

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos.")

    def estadisticas(self):
        if not self.numeros:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        try:
            alpha = float(self.alpha_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para el nivel de confianza.")
            return

        media = np.mean(self.numeros)
        varianza = np.var(self.numeros)

        n = len(self.numeros)

        # --- Prueba de medias ---
        z0 = (media - 0.5) * np.sqrt(12*n)
        z_alpha = norm.ppf(1 - alpha/2)

        # --- Prueba de varianza ---
        chi2_calculado = (n - 1) * varianza / (1/12)
        chi2_inf = chi2.ppf(alpha/2, n-1)
        chi2_sup = chi2.ppf(1 - alpha/2, n-1)

        # --- Prueba de uniformidad (Chi-cuadrado) ---
        k = 10
        frec_obs, _ = np.histogram(self.numeros, bins=k)
        fe = n / k
        chi2_uniform = np.sum((frec_obs - fe)**2 / fe)
        chi2_crit = chi2.ppf(1 - alpha, k - 1)

        resultado = f"""
        Media: {media:.4f}
        Varianza: {varianza:.4f}

        🔹 Prueba de medias:
        Z0 = {z0:.4f}, Zα = ±{z_alpha:.4f}
        {'✅ Pasa' if abs(z0) < z_alpha else '❌ Rechazado'}

        🔹 Prueba de varianza:
        χ² = {chi2_calculado:.4f}, IC = [{chi2_inf:.4f}, {chi2_sup:.4f}]
        {'✅ Pasa' if chi2_inf < chi2_calculado < chi2_sup else '❌ Rechazado'}

        🔹 Prueba de uniformidad:
        χ² = {chi2_uniform:.4f}, χ² crítico = {chi2_crit:.4f}
        {'✅ Pasa' if chi2_uniform < chi2_crit else '❌ Rechazado'}
        """

        messagebox.showinfo("Resultados estadísticos", resultado)

    def estadisticas(self):
        if not self.numeros:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        try:
            alpha = float(self.alpha_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para el nivel de confianza.")
            return

        media = np.mean(self.numeros)

        varianza = np.var(self.numeros, ddof=1)

        n = len(self.numeros)

        z = norm.ppf(1 - alpha / 2)
        limite_inf_media = 0.5 - (z * (1 / np.sqrt(12*n)))
        limite_sup_media = 0.5 + (z * (1 / np.sqrt(12*n)))


        # --- Prueba de varianza ---
        chi2_calculado = (n - 1) * varianza / (1/12)
        chi2_sup = chi2.ppf(alpha/2, n-1)
        chi2_inf = chi2.ppf(1 - alpha/2, n-1)
        a=int(12*(n-1))

        limite_inf_var = chi2_sup/a
        limite_sup_var = chi2_inf/a

        # --- Prueba de uniformidad (Chi-cuadrado) ---
        k = 10
        frec_obs, _ = np.histogram(self.numeros, bins=k)
        fe = n / k
        chi2_uniform = np.sum((frec_obs - fe)**2 / fe)
        chi2_crit = chi2.ppf(1 - alpha, k - 1)


        resultado = f"""
        ---Media: {media:.4f}
        ---Limite Superior: {limite_sup_media:.4f}
        ---Limite Inferior: {limite_inf_media:.4f}
        
        * Prueba de Medias:
        χ² = {media:.4f}, L = [{limite_inf_media:.4f}, {limite_sup_media:.4f}]
        {'✅ Pasa' if limite_inf_media < media < limite_sup_media else '❌ Rechazado'}
        
        ---Varianza: {varianza:.4f}
        ---Limite Superior: {limite_sup_var:.4f}
        ---Limite Inferior: {limite_inf_var:.4f}
        * Prueba de Varianza:
        V = {varianza:.4f}, L = [{limite_inf_var:.4f}, {limite_sup_var:.4f}]
        {'✅ Pasa' if limite_inf_var < varianza < limite_sup_var else '❌ Rechazado'}
        

        * Prueba de uniformidad:
        χ² = {chi2_uniform:.4f}, χ² crítico = {chi2_crit:.4f}
        {'✅ Pasa' if chi2_uniform < chi2_crit else '❌ Rechazado'}
        """

        messagebox.showinfo("Resultados estadísticos", resultado)


    def histogramas(self):
        if not self.numeros:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        # Histograma de números
        axs[0,0].hist(self.numeros, bins=10, edgecolor='black')
        axs[0,0].set_title("Histograma - Números generados")

        # Histograma de medias (valores centrados en 0.5)
        axs[0,1].hist([x-0.5 for x in self.numeros], bins=10, edgecolor='black')
        axs[0,1].set_title("Histograma - Desviación de medias")

        # Histograma de varianza (distribución de cuadrados)
        axs[1,0].hist([(x-0.5)**2 for x in self.numeros], bins=10, edgecolor='black')
        axs[1,0].set_title("Histograma - Varianza (xi-0.5)^2")

        # Histograma de uniformidad (frecuencias observadas)
        axs[1,1].hist(self.numeros, bins=10, edgecolor='black')
        axs[1,1].set_title("Histograma - Uniformidad")

        plt.tight_layout()
        plt.show()

    def exportar(self):
        if not self.iteraciones:
            messagebox.showwarning("Atención", "Primero genere los números.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Texto", "*.txt"),
                                                          ("Excel", "*.xlsx"),
                                                          ("Word (RTF)", "*.rtf")])
        if not archivo:
            return

        if archivo.endswith(".txt"):
            with open(archivo, "w") as f:
                for it in self.iteraciones:
                    f.write(f"Iter {it[0]}: producto={it[1]}, centro={it[2]}, decimal={it[3]}\n")

        elif archivo.endswith(".xlsx"):
            df = pd.DataFrame(self.iteraciones, columns=["Iteración", "Producto", "Centro", "Número"])
            df.to_excel(archivo, index=False)

        elif archivo.endswith(".rtf"):
            contenido = "\n".join([f"Iter {it[0]}: producto={it[1]}, centro={it[2]}, decimal={it[3]}" for it in self.iteraciones])
            pypandoc.convert_text(contenido, "rtf", format="md", outputfile=archivo, extra_args=["--standalone"])

        messagebox.showinfo("Exportación", f"Archivo guardado en {archivo}")

    def abrir_modulo(self, archivo):
        """Ejecuta otro script Python y cierra la ventana actual."""
        ruta = os.path.join(os.path.dirname(__file__), archivo)
        if os.path.exists(ruta):
            self.root.destroy()  # Cierra la ventana actual
            subprocess.Popen([sys.executable, ruta])
        else:
            messagebox.showerror("Error", f"No se encontró el archivo: {archivo}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorApp(root)
    root.mainloop()
