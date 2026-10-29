import tkinter as tk
from tkinter import ttk, messagebox


class Nodo:
    """Nodo del arbol binario de busqueda."""
    def __init__(self, codigo, titulo, autor):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.izquierdo = None
        self.derecho = None


class ArbolBinarioBusqueda:
    """Organiza los libros por codigo usando un arbol binario de busqueda."""
    def __init__(self):
        self.raiz = None

    def insertar(self, codigo, titulo, autor):
        codigo = int(codigo)
        nuevo = Nodo(codigo, titulo, autor)

        if self.raiz is None:
            self.raiz = nuevo
            return True

        actual = self.raiz
        while True:
            if codigo == actual.codigo:
                return False
            elif codigo < actual.codigo:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    return True
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    return True
                actual = actual.derecho

    def buscar(self, codigo):
        codigo = int(codigo)
        actual = self.raiz
        while actual is not None:
            if codigo == actual.codigo:
                return actual
            actual = actual.izquierdo if codigo < actual.codigo else actual.derecho
        return None

    def _minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def _eliminar(self, nodo, codigo):
        if nodo is None:
            return None, False

        if codigo < nodo.codigo:
            nodo.izquierdo, eliminado = self._eliminar(nodo.izquierdo, codigo)
            return nodo, eliminado
        if codigo > nodo.codigo:
            nodo.derecho, eliminado = self._eliminar(nodo.derecho, codigo)
            return nodo, eliminado

        # Caso 1: el nodo no tiene hijos o tiene solo uno.
        if nodo.izquierdo is None:
            return nodo.derecho, True
        if nodo.derecho is None:
            return nodo.izquierdo, True

        # Caso 2: tiene dos hijos; se reemplaza por su sucesor.
        sucesor = self._minimo(nodo.derecho)
        nodo.codigo = sucesor.codigo
        nodo.titulo = sucesor.titulo
        nodo.autor = sucesor.autor
        nodo.derecho, _ = self._eliminar(nodo.derecho, sucesor.codigo)
        return nodo, True

    def eliminar(self, codigo):
        codigo = int(codigo)
        self.raiz, eliminado = self._eliminar(self.raiz, codigo)
        return eliminado

    def recorrer_inorden(self):
        libros = []

        def recorrido(nodo):
            if nodo is not None:
                recorrido(nodo.izquierdo)
                libros.append(nodo)
                recorrido(nodo.derecho)

        recorrido(self.raiz)
        return libros


class BibliotecaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("BibliotecaTree - Gestion de libros")
        self.ventana.geometry("850x570")
        self.ventana.minsize(760, 500)

        self.arbol = ArbolBinarioBusqueda()
        self._crear_interfaz()

        # Datos de ejemplo para demostrar el funcionamiento.
        ejemplos = [
            ("50", "Cien años de soledad", "Gabriel Garcia Marquez"),
            ("30", "El principito", "Antoine de Saint-Exupery"),
            ("70", "Don Quijote de la Mancha", "Miguel de Cervantes"),
            ("20", "La ciudad y los perros", "Mario Vargas Llosa"),
            ("40", "Cronica de una muerte anunciada", "Gabriel Garcia Marquez"),
            ("60", "La odisea", "Homero"),
            ("80", "Romeo y Julieta", "William Shakespeare"),
        ]
        for codigo, titulo, autor in ejemplos:
            self.arbol.insertar(codigo, titulo, autor)
        self._actualizar_tabla()

    def _crear_interfaz(self):
        encabezado = ttk.Label(
            self.ventana,
            text="BibliotecaTree",
            font=("Arial", 22, "bold")
        )
        encabezado.pack(pady=(15, 2))

        subtitulo = ttk.Label(
            self.ventana,
            text="Sistema de gestion de libros con arbol binario de busqueda"
        )
        subtitulo.pack(pady=(0, 12))

        formulario = ttk.LabelFrame(self.ventana, text="Datos del libro", padding=12)
        formulario.pack(fill="x", padx=18, pady=5)

        ttk.Label(formulario, text="Codigo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.codigo_var = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.codigo_var, width=18).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(formulario, text="Titulo:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.titulo_var = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.titulo_var, width=28).grid(
            row=0, column=3, padx=5, pady=5
        )

        ttk.Label(formulario, text="Autor:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.autor_var = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.autor_var, width=28).grid(
            row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5
        )

        botones = ttk.Frame(self.ventana)
        botones.pack(fill="x", padx=18, pady=8)

        ttk.Button(botones, text="Agregar libro", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar por codigo", command=self.buscar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar libro", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self._actualizar_tabla).pack(side="left", padx=4)

        marco_tabla = ttk.LabelFrame(self.ventana, text="Libros registrados (ordenados por codigo)", padding=10)
        marco_tabla.pack(fill="both", expand=True, padx=18, pady=8)

        columnas = ("codigo", "titulo", "autor")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        self.tabla.heading("codigo", text="Codigo")
        self.tabla.heading("titulo", text="Titulo")
        self.tabla.heading("autor", text="Autor")
        self.tabla.column("codigo", width=100, anchor="center")
        self.tabla.column("titulo", width=330)
        self.tabla.column("autor", width=260)

        barra = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.estado_var = tk.StringVar(value="Listo. Los libros se almacenan en un arbol binario de busqueda.")
        ttk.Label(self.ventana, textvariable=self.estado_var, relief="sunken", anchor="w").pack(
            fill="x", side="bottom"
        )

    def _obtener_codigo(self):
        codigo = self.codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Dato requerido", "Ingresa el codigo del libro.")
            return None
        try:
            return int(codigo)
        except ValueError:
            messagebox.showwarning("Codigo invalido", "El codigo debe ser un numero entero.")
            return None

    def agregar(self):
        codigo = self._obtener_codigo()
        if codigo is None:
            return

        titulo = self.titulo_var.get().strip()
        autor = self.autor_var.get().strip()
        if not titulo or not autor:
            messagebox.showwarning("Datos requeridos", "Ingresa el titulo y el autor.")
            return

        if self.arbol.insertar(codigo, titulo, autor):
            self._actualizar_tabla()
            self.estado_var.set(f"Libro {codigo} agregado correctamente.")
            self.limpiar()
        else:
            messagebox.showerror("Codigo duplicado", "Ya existe un libro con ese codigo.")

    def buscar(self):
        codigo = self._obtener_codigo()
        if codigo is None:
            return

        libro = self.arbol.buscar(codigo)
        if libro:
            self.titulo_var.set(libro.titulo)
            self.autor_var.set(libro.autor)
            self.estado_var.set(f"Libro encontrado: {libro.titulo}")
            self.tabla.selection_set(str(codigo))
            self.tabla.see(codigo)
        else:
            messagebox.showinfo("Resultado", "No se encontro un libro con ese codigo.")
            self.estado_var.set(f"No existe el codigo {codigo}.")

    def eliminar(self):
        codigo = self._obtener_codigo()
        if codigo is None:
            return

        if self.arbol.eliminar(codigo):
            self._actualizar_tabla()
            self.estado_var.set(f"Libro {codigo} eliminado correctamente.")
            self.limpiar()
        else:
            messagebox.showinfo("Resultado", "No existe un libro con ese codigo.")

    def _actualizar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        for libro in self.arbol.recorrer_inorden():
            self.tabla.insert(
                "", "end", iid=str(libro.codigo),
                values=(libro.codigo, libro.titulo, libro.autor)
            )
        self.estado_var.set(f"Total de libros registrados: {len(self.arbol.recorrer_inorden())}")

    def limpiar(self):
        self.codigo_var.set("")
        self.titulo_var.set("")
        self.autor_var.set("")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = BibliotecaApp(ventana)
    ventana.mainloop()
