import sys
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Union
import json

class FinancialManager:
    def __init__(self):
        self.csv_file = "financial_data.csv"
        self.config_file = "config.json"
        self.categories = self.load_categories()
        self.setup_main_window()
        self.initialize_csv()
        self.create_widgets()
        self.load_data()
        self.update_historical_totals()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def show_category_config(self):
        def save_callback(new_categories):
            self.categories = new_categories
            # Guardar en el archivo de configuración
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, indent=4)
            # Actualizar el combobox de categorías
            self.update_category_options()

        CategoryManager(self.root, self.categories, save_callback)

    def load_categories(self) -> Dict[str, List[str]]:
        default_categories = {
            "Ingreso": ["Salario", "Inversiones", "Otros"],
            "Egreso": ["Alimentación", "Transporte", "Servicios", "Otros"],
            "Activo": ["Efectivo", "Inversiones", "Propiedades", "Otros"],
            "Pasivo": ["Préstamos", "Tarjetas", "Hipoteca", "Otros"]
        }
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_categories, f, indent=4)
            return default_categories

    def setup_main_window(self):
        self.root = tk.Tk()
        self.root.title("Gestor Financiero")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.setup_styles()
        try:
            icon = tk.PhotoImage(file=self.resource_path("icono.png"))
            self.root.iconphoto(True, icon)
        except tk.TclError:
            pass

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Define custom colors
        self.colors = {
            "primary": "#2c3e50",
            "secondary": "#34495e",
            "accent": "#3498db",
            "success": "#2ecc71",
            "warning": "#f1c40f",
            "danger": "#e74c3c",
            "background": "#ecf0f1"
        }

        # Configure styles
        self.style.configure(
            "Custom.TButton",
            background=self.colors["accent"],
            foreground="white",
            padding=10,
            font=("Helvetica", 10, "bold")
        )
        
        self.style.configure(
            "Custom.Treeview",
            background="white",
            fieldbackground="white",
            foreground=self.colors["primary"],
            rowheight=30
        )

    def initialize_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Tipo", "Descripción", "Monto", "Categoría", "Fecha", "Notas"])

    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create frames
        self.create_input_summary_frame()
        self.create_filter_frame()
        self.create_table_frame()

    def create_input_summary_frame(self):
        input_summary_frame = ttk.Frame(self.main_container)
        input_summary_frame.pack(fill=tk.X, pady=(0, 10))

        # Nueva Entrada
        self.create_input_frame(input_summary_frame)

        # Resumen
        self.create_summary_frame(input_summary_frame)

    def create_input_frame(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Nueva Entrada", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Variables
        self.tipo_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.monto_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.fecha_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.notas_var = tk.StringVar()

        # Grid layout for input fields
        self.create_input_fields(input_frame)

    def create_summary_frame(self, parent):
        summary_frame = ttk.LabelFrame(parent, text="Resumen", padding=10)
        summary_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Summary variables
        self.summary_vars = {
            "Ingresos": tk.StringVar(),
            "Egresos": tk.StringVar(),
            "Balance": tk.StringVar(),
            "Activos": tk.StringVar(),
            "Pasivos": tk.StringVar()
        }

        # Create summary labels
        for i, (key, var) in enumerate(self.summary_vars.items()):
            ttk.Label(summary_frame, text=f"{key}:").grid(row=0, column=i*2, padx=5, pady=5)
            ttk.Label(summary_frame, textvariable=var).grid(row=0, column=i*2+1, padx=5, pady=5)

    def create_input_fields(self, frame):
        # Tipo
        ttk.Label(frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
        tipo_combo = ttk.Combobox(frame, textvariable=self.tipo_var, values=list(self.categories.keys()), state="readonly")
        tipo_combo.grid(row=0, column=1, padx=5, pady=5)
        tipo_combo.bind('<<ComboboxSelected>>', self.update_category_options)

        # Descripción
        ttk.Label(frame, text="Descripción:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.descripcion_var).grid(row=0, column=3, padx=5, pady=5)

        # Monto
        ttk.Label(frame, text="Monto:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.monto_var).grid(row=1, column=1, padx=5, pady=5)

        # Categoría
        ttk.Label(frame, text="Categoría:").grid(row=1, column=2, padx=5, pady=5)
        self.categoria_combo = ttk.Combobox(frame, textvariable=self.categoria_var, state="readonly")
        self.categoria_combo.grid(row=1, column=3, padx=5, pady=5)

        # Fecha
        ttk.Label(frame, text="Fecha:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.fecha_var).grid(row=2, column=1, padx=5, pady=5)

        # Notas
        ttk.Label(frame, text="Notas:").grid(row=2, column=2, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.notas_var).grid(row=2, column=3, padx=5, pady=5)

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Agregar", command=self.add_entry, style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_entries, style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        # Agregar el nuevo botón aquí:
        ttk.Button(button_frame, text="Configurar Categorías", 
                command=self.show_category_config, 
                style="Custom.TButton").pack(side=tk.LEFT, padx=5)

    def create_filter_frame(self):
        filter_frame = ttk.LabelFrame(self.main_container, text="Filtros", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        # Variables
        self.month_var = tk.StringVar(value=datetime.now().strftime("%m"))
        self.year_var = tk.StringVar(value=datetime.now().strftime("%Y"))

        # Month and Year filters
        ttk.Label(filter_frame, text="Mes:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.month_var, 
                    values=[f"{i:02d}" for i in range(1, 13)], 
                    state="readonly", width=5).pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="Año:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.year_var,
                    values=[str(i) for i in range(datetime.now().year, 2000, -1)],
                    state="readonly", width=6).pack(side=tk.LEFT, padx=5)

        # Filter buttons
        ttk.Button(filter_frame, text="Filtrar", 
                  command=self.filter_data, 
                  style="Custom.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Ver Gráficos", 
                  command=self.show_graphs,
                  style="Custom.TButton").pack(side=tk.LEFT, padx=5)

    def create_table_frame(self):
        table_frame = ttk.LabelFrame(self.main_container, text="Registros", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview
        columns = ("Tipo", "Descripción", "Monto", "Categoría", "Fecha", "Notas")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview")

        # Configure columns
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(fill=tk.BOTH, expand=True)

    def update_category_options(self, event=None):
        tipo = self.tipo_var.get()
        if (tipo in self.categories):
            self.categoria_combo['values'] = self.categories[tipo]
            self.categoria_combo.set('')

    def add_entry(self):
        # Validación de datos
        if not self.validate_entry():
            return

        # Agregar entrada al CSV
        with open(self.csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.tipo_var.get(),
                self.descripcion_var.get(),
                self.monto_var.get(),
                self.categoria_var.get(),
                self.fecha_var.get(),
                self.notas_var.get()
            ])

        self.load_data()
        self.clear_entries()
        self.update_historical_totals()
        messagebox.showinfo("Éxito", "Entrada agregada correctamente")

    def validate_entry(self) -> bool:
        # Validar campos requeridos
        required_fields = {
            "Tipo": self.tipo_var.get(),
            "Descripción": self.descripcion_var.get(),
            "Monto": self.monto_var.get(),
            "Categoría": self.categoria_var.get(),
            "Fecha": self.fecha_var.get()
        }

        for field, value in required_fields.items():
            if not value:
                messagebox.showerror("Error", f"El campo {field} es requerido")
                return False

        # Validar monto
        try:
            float(self.monto_var.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
            return False

        # Validar fecha
        try:
            fecha = datetime.strptime(self.fecha_var.get(), "%d/%m/%Y")
            if fecha > datetime.now():
                messagebox.showerror("Error", "La fecha no puede ser futura")
                return False
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido (DD/MM/YYYY)")
            return False

        return True

    def clear_entries(self):
        self.tipo_var.set('')
        self.descripcion_var.set('')
        self.monto_var.set('')
        self.categoria_var.set('')
        self.fecha_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.notas_var.set('')

    def load_data(self):
        # Limpiar tabla
        for item in self.table.get_children():
            self.table.delete(item)

        # Cargar datos del CSV
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    self.table.insert("", tk.END, values=row)

    def filter_data(self):
        month = self.month_var.get()
        year = self.year_var.get()

        # Limpiar tabla
        for item in self.table.get_children():
            self.table.delete(item)

        # Cargar datos filtrados
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    fecha = datetime.strptime(row[4], "%d/%m/%Y")
                    if (fecha.strftime("%m") == month and 
                        fecha.strftime("%Y") == year):
                        self.table.insert("", tk.END, values=row)

        self.update_summary()

    def update_summary(self):
        totals = {
            "Ingresos": 0,
            "Egresos": 0,
            "Activos": 0,
            "Pasivos": 0
        }

        for item in self.table.get_children():
            values = self.table.item(item)['values']
            tipo = values[0]
            monto = float(values[2])

            if tipo == "Ingreso":
                totals["Ingresos"] += monto
            elif tipo == "Egreso":
                totals["Egresos"] += monto
            elif tipo == "Activo":
                totals["Activos"] += monto
            elif tipo == "Pasivo":
                totals["Pasivos"] += monto

# Actualizar variables de resumen
        self.summary_vars["Ingresos"].set(f"${totals['Ingresos']:,.2f}")
        self.summary_vars["Egresos"].set(f"${totals['Egresos']:,.2f}")
        self.summary_vars["Balance"].set(f"${totals['Ingresos'] - totals['Egresos']:,.2f}")
        self.summary_vars["Activos"].set(f"${totals['Activos']:,.2f}")
        self.summary_vars["Pasivos"].set(f"${totals['Pasivos']:,.2f}")

    def update_historical_totals(self):
        totals = {
            "Ingresos": 0,
            "Egresos": 0,
            "Activos": 0,
            "Pasivos": 0
        }

        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    tipo = row[0]
                    monto = float(row[2])
                    
                    if tipo == "Ingreso":
                        totals["Ingresos"] += monto
                    elif tipo == "Egreso":
                        totals["Egresos"] += monto
                    elif tipo == "Activo":
                        totals["Activos"] += monto
                    elif tipo == "Pasivo":
                        totals["Pasivos"] += monto

        self.update_summary_with_totals(totals)

    def update_summary_with_totals(self, totals: Dict[str, float]):
        for key, value in totals.items():
            self.summary_vars[key].set(f"${value:,.2f}")
        self.summary_vars["Balance"].set(
            f"${totals['Ingresos'] - totals['Egresos']:,.2f}"
        )

    def show_graphs(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Análisis Gráfico")
        graph_window.geometry("1000x600")

        notebook = ttk.Notebook(graph_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear pestañas para diferentes gráficos
        self.create_monthly_analysis_tab(notebook)
        self.create_category_analysis_tab(notebook)
        self.create_trend_analysis_tab(notebook)

    def create_monthly_analysis_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Análisis Mensual")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Datos para los gráficos
        data = self.get_monthly_data()
        
        # Gráfico de barras - Ingresos vs Egresos
        months = data.keys()
        ingresos = [d['Ingresos'] for d in data.values()]
        egresos = [d['Egresos'] for d in data.values()]
        
        x = range(len(months))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], ingresos, width, label='Ingresos', color='green')
        ax1.bar([i + width/2 for i in x], egresos, width, label='Egresos', color='red')
        ax1.set_title('Ingresos vs Egresos por Mes')
        ax1.set_xticks(x)
        ax1.set_xticklabels(months, rotation=45)
        ax1.legend()
        
        # Gráfico de línea - Balance Neto
        balance = [d['Ingresos'] - d['Egresos'] for d in data.values()]
        ax2.plot(months, balance, marker='o', color='blue')
        ax2.set_title('Balance Neto por Mes')
        ax2.set_xticklabels(months, rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_category_analysis_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Análisis por Categoría")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Datos para los gráficos
        categoria_data = self.get_category_data()
        
        # Gráfico de torta - Ingresos por categoría
        ingresos = categoria_data['Ingreso']
        if ingresos:
            ax1.pie(ingresos.values(), labels=ingresos.keys(), autopct='%1.1f%%')
            ax1.set_title('Distribución de Ingresos')
        
        # Gráfico de torta - Egresos por categoría
        egresos = categoria_data['Egreso']
        if egresos:
            ax2.pie(egresos.values(), labels=egresos.keys(), autopct='%1.1f%%')
            ax2.set_title('Distribución de Egresos')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_trend_analysis_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Análisis de Tendencias")

        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Datos para el gráfico
        data = self.get_monthly_data()
        months = list(data.keys())
        
        # Crear líneas de tendencia para diferentes métricas
        metrics = ['Ingresos', 'Egresos', 'Activos', 'Pasivos']
        colors = ['green', 'red', 'blue', 'orange']
        
        for metric, color in zip(metrics, colors):
            values = [d[metric] for d in data.values()]
            ax.plot(months, values, marker='o', label=metric, color=color)
        
        ax.set_title('Tendencias Financieras')
        ax.set_xticklabels(months, rotation=45)
        ax.legend()
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_monthly_data(self) -> Dict[str, Dict[str, float]]:
        data = {}
        
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    fecha = datetime.strptime(row[4], "%d/%m/%Y")
                    mes = fecha.strftime("%b %Y")
                    tipo = row[0]
                    monto = float(row[2])
                    
                    if mes not in data:
                        data[mes] = {
                            "Ingresos": 0,
                            "Egresos": 0,
                            "Activos": 0,
                            "Pasivos": 0
                        }
                    
                    if tipo == "Ingreso":
                        data[mes]["Ingresos"] += monto
                    elif tipo == "Egreso":
                        data[mes]["Egresos"] += monto
                    elif tipo == "Activo":
                        data[mes]["Activos"] += monto
                    elif tipo == "Pasivo":
                        data[mes]["Pasivos"] += monto
        
        return dict(sorted(data.items()))

    def get_category_data(self) -> Dict[str, Dict[str, float]]:
        data = {
            "Ingreso": {},
            "Egreso": {},
            "Activo": {},
            "Pasivo": {}
        }
        
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    tipo = row[0]
                    categoria = row[3]
                    monto = float(row[2])
                    
                    if categoria not in data[tipo]:
                        data[tipo][categoria] = 0
                    data[tipo][categoria] += monto
    
    
        
        return data
    
class CategoryManager:
    def __init__(self, parent, categories, save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuración de Categorías")
        self.window.geometry("600x400")
        self.categories = categories.copy()
        self.save_callback = save_callback
        self.create_widgets()

    def create_widgets(self):
        # Notebook para pestañas de tipos
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Crear una pestaña para cada tipo
        self.tabs = {}
        for tipo in self.categories.keys():
            self.create_type_tab(tipo)

        # Botones de guardar y cancelar
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save_categories).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=5)

    def create_type_tab(self, tipo):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tipo)
        
        # Frame para la lista y botones
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Lista de categorías
        self.tabs[tipo] = {
            'listbox': tk.Listbox(list_frame, selectmode=tk.SINGLE),
            'categories': self.categories[tipo]
        }
        
        listbox = self.tabs[tipo]['listbox']
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # Cargar categorías existentes
        for category in self.categories[tipo]:
            listbox.insert(tk.END, category)

        # Botones
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="Agregar", 
                  command=lambda t=tipo: self.add_category(t)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Editar", 
                  command=lambda t=tipo: self.edit_category(t)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", 
                  command=lambda t=tipo: self.delete_category(t)).pack(side=tk.LEFT, padx=5)

    def add_category(self, tipo):
        dialog = tk.Toplevel(self.window)
        dialog.title("Agregar Categoría")
        dialog.geometry("300x100")
        dialog.transient(self.window)
        dialog.grab_set()

        ttk.Label(dialog, text="Nombre de la categoría:").pack(padx=10, pady=5)
        entry = ttk.Entry(dialog)
        entry.pack(padx=10, pady=5)

        def save():
            name = entry.get().strip()
            if name:
                if name not in self.tabs[tipo]['categories']:
                    self.tabs[tipo]['listbox'].insert(tk.END, name)
                    self.tabs[tipo]['categories'].append(name)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Esta categoría ya existe")
            else:
                messagebox.showerror("Error", "El nombre no puede estar vacío")

        ttk.Button(dialog, text="Guardar", command=save).pack(pady=5)

    def edit_category(self, tipo):
        selection = self.tabs[tipo]['listbox'].curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor selecciona una categoría para editar")
            return

        index = selection[0]
        old_name = self.tabs[tipo]['listbox'].get(index)

        dialog = tk.Toplevel(self.window)
        dialog.title("Editar Categoría")
        dialog.geometry("300x100")
        dialog.transient(self.window)
        dialog.grab_set()

        ttk.Label(dialog, text="Nuevo nombre:").pack(padx=10, pady=5)
        entry = ttk.Entry(dialog)
        entry.insert(0, old_name)
        entry.pack(padx=10, pady=5)

        def save():
            new_name = entry.get().strip()
            if new_name:
                if new_name != old_name and new_name in self.tabs[tipo]['categories']:
                    messagebox.showerror("Error", "Esta categoría ya existe")
                    return
                self.tabs[tipo]['listbox'].delete(index)
                self.tabs[tipo]['listbox'].insert(index, new_name)
                self.tabs[tipo]['categories'][self.tabs[tipo]['categories'].index(old_name)] = new_name
                dialog.destroy()
            else:
                messagebox.showerror("Error", "El nombre no puede estar vacío")

        ttk.Button(dialog, text="Guardar", command=save).pack(pady=5)

    def delete_category(self, tipo):
        selection = self.tabs[tipo]['listbox'].curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor selecciona una categoría para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta categoría?"):
            index = selection[0]
            category = self.tabs[tipo]['listbox'].get(index)
            self.tabs[tipo]['listbox'].delete(index)
            self.tabs[tipo]['categories'].remove(category)

    def save_categories(self):
        # Actualizar diccionario de categorías
        for tipo in self.categories:
            self.categories[tipo] = list(self.tabs[tipo]['categories'])
        
        # Llamar al callback con las nuevas categorías
        self.save_callback(self.categories)
        self.window.destroy()

if __name__ == "__main__":
    app = FinancialManager()
    app.root.mainloop()