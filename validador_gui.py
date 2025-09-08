# Interfaz gráfica para validar número de celular y correo electrónico
# Autor: Alejandro
# Fecha: 2025-09-07

import tkinter as tk
from tkinter import messagebox
from validador_celular_colombia import validar_numero_colombia
from validador_correo_electronico import validar_correo_electronico

class ValidadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Celular y Correo")
        self.root.geometry("350x250")
        self.modo = tk.StringVar(value="celular")
        self.crear_widgets()

    def crear_widgets(self):
        # Selector de modo
        frame_modo = tk.Frame(self.root)
        frame_modo.pack(pady=10)
        tk.Radiobutton(frame_modo, text="Validar Celular", variable=self.modo, value="celular", command=self.cambiar_modo).pack(side=tk.LEFT)
        tk.Radiobutton(frame_modo, text="Validar Correo", variable=self.modo, value="correo", command=self.cambiar_modo).pack(side=tk.LEFT)

        # Etiqueta y entrada
        self.label = tk.Label(self.root, text="Ingrese el número de celular:")
        self.label.pack(pady=5)
        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=5)

        # Botón de validación
        self.btn_validar = tk.Button(self.root, text="Validar", command=self.validar)
        self.btn_validar.pack(pady=10)

    def cambiar_modo(self):
        if self.modo.get() == "celular":
            self.label.config(text="Ingrese el número de celular:")
            self.entry.delete(0, tk.END)
        else:
            self.label.config(text="Ingrese el correo electrónico:")
            self.entry.delete(0, tk.END)

    def validar(self):
        valor = self.entry.get().strip()
        if self.modo.get() == "celular":
            if validar_numero_colombia(valor):
                messagebox.showinfo("Resultado", f"{valor} es un número de celular válido.")
            else:
                messagebox.showerror("Resultado", f"{valor} NO es un número de celular válido.")
        else:
            if validar_correo_electronico(valor):
                messagebox.showinfo("Resultado", f"{valor} es un correo electrónico válido.")
            else:
                messagebox.showerror("Resultado", f"{valor} NO es un correo electrónico válido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidadorApp(root)
    root.mainloop()
