import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os

try:
    import wrapper
except ImportError:
    print("ERROR: El módulo wrapper no está compilado.")
    print("Por favor ejecuta: python setup.py build_ext --inplace")
    exit(1)

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ImportError:
    print("ERROR: Faltan dependencias de visualización.")
    print("Instala con: pip install networkx matplotlib")
    exit(1)


class NeuroNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Grafos Masivos")
        self.root.geometry("1200x800")
        
        self.grafo = None
        self.archivo_actual = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame superior - Controles
        frame_control = ttk.Frame(self.root, padding="10")
        frame_control.pack(fill=tk.X)
        
        # Botón cargar archivo
        ttk.Button(frame_control, text="📁 Cargar Dataset", 
                   command=self.cargar_archivo).pack(side=tk.LEFT, padx=5)
        
        # Botón nodo crítico
        ttk.Button(frame_control, text="🎯 Nodo Más Crítico", 
                   command=self.encontrar_nodo_critico).pack(side=tk.LEFT, padx=5)
        
        # Frame para BFS
        ttk.Label(frame_control, text="Nodo Inicio:").pack(side=tk.LEFT, padx=5)
        self.entry_nodo = ttk.Entry(frame_control, width=10)
        self.entry_nodo.insert(0, "0")
        self.entry_nodo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_control, text="Profundidad:").pack(side=tk.LEFT, padx=5)
        self.entry_prof = ttk.Entry(frame_control, width=10)
        self.entry_prof.insert(0, "2")
        self.entry_prof.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_control, text="🔍 Ejecutar BFS", 
                   command=self.ejecutar_bfs).pack(side=tk.LEFT, padx=5)
        
        # Frame de métricas
        frame_metricas = ttk.LabelFrame(self.root, text="📊 Métricas del Grafo", 
                                        padding="10")
        frame_metricas.pack(fill=tk.X, padx=10, pady=5)
        
        self.label_archivo = ttk.Label(frame_metricas, 
                                       text="Archivo: No cargado")
        self.label_archivo.pack(anchor=tk.W)
        
        self.label_nodos = ttk.Label(frame_metricas, 
                                     text="Nodos: 0")
        self.label_nodos.pack(anchor=tk.W)
        
        self.label_aristas = ttk.Label(frame_metricas, 
                                       text="Aristas: 0")
        self.label_aristas.pack(anchor=tk.W)
        
        self.label_memoria = ttk.Label(frame_metricas, 
                                       text="Tiempo de carga: 0 s")
        self.label_memoria.pack(anchor=tk.W)
        
        self.label_critico = ttk.Label(frame_metricas, 
                                       text="Nodo más crítico: N/A")
        self.label_critico.pack(anchor=tk.W)
        
        # Frame de visualización
        frame_viz = ttk.LabelFrame(self.root, text="🗺️ Visualización", 
                                   padding="10")
        frame_viz.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Canvas de matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_viz)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Texto inicial
        self.ax.text(0.5, 0.5, 'Carga un dataset para comenzar', 
                    ha='center', va='center', fontsize=14, 
                    transform=self.ax.transAxes)
        self.ax.set_axis_off()
        self.canvas.draw()
        
        # Consola de logs
        frame_log = ttk.LabelFrame(self.root, text="📝 Log de Operaciones", 
                                   padding="5")
        frame_log.pack(fill=tk.X, padx=10, pady=5)
        
        self.text_log = tk.Text(frame_log, height=8, state=tk.DISABLED)
        self.text_log.pack(fill=tk.X)
        
        scrollbar = ttk.Scrollbar(self.text_log)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_log.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_log.yview)
    
    def log(self, mensaje):
        """Agregar mensaje al log"""
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, mensaje + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)
        self.root.update()
    
    def cargar_archivo(self):
        """Cargar archivo de dataset"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[("Archivos de Texto", "*.txt"), 
                      ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        self.log(f"🔄 Cargando archivo: {os.path.basename(archivo)}")
        
        try:
            self.grafo = wrapper.PyGrafoDisperso()
            
            inicio = time.time()
            if not self.grafo.cargar_datos(archivo):
                messagebox.showerror("Error", "No se pudo cargar el archivo")
                return
            fin = time.time()
            
            self.archivo_actual = archivo
            tiempo_carga = fin - inicio
            
            # Actualizar métricas
            self.label_archivo.config(
                text=f"Archivo: {os.path.basename(archivo)}")
            self.label_nodos.config(
                text=f"Nodos: {self.grafo.obtener_num_nodos():,}")
            self.label_aristas.config(
                text=f"Aristas: {self.grafo.obtener_num_aristas():,}")
            self.label_memoria.config(
                text=f"Tiempo de carga: {tiempo_carga:.3f} s")
            
            self.log(f"✅ Dataset cargado exitosamente")
            self.log(f"   Nodos: {self.grafo.obtener_num_nodos():,}")
            self.log(f"   Aristas: {self.grafo.obtener_num_aristas():,}")
            self.log(f"   Tiempo: {tiempo_carga:.3f} segundos")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {str(e)}")
            self.log(f"❌ Error: {str(e)}")
    
    def encontrar_nodo_critico(self):
        """Encontrar y visualizar el nodo con mayor grado"""
        if not self.grafo:
            messagebox.showwarning("Advertencia", 
                                  "Primero debes cargar un dataset")
            return
        
        self.log("🎯 Buscando nodo más crítico...")
        
        try:
            nodo_max = self.grafo.encontrar_nodo_max_grado()
            grado = self.grafo.obtener_grado(nodo_max)
            
            self.label_critico.config(
                text=f"Nodo más crítico: {nodo_max} (Grado: {grado:,})")
            
            self.log(f"✅ Nodo más crítico: {nodo_max}")
            self.log(f"   Grado: {grado:,} conexiones")
            
            # Visualizar el nodo y sus vecinos inmediatos
            self.visualizar_nodo_critico(nodo_max)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.log(f"❌ Error: {str(e)}")
    
    def visualizar_nodo_critico(self, nodo):
        """Visualizar un nodo y sus vecinos"""
        vecinos = self.grafo.get_vecinos(nodo)
        
        # Limitar visualización a primeros 100 vecinos
        vecinos = vecinos[:100]
        
        # Crear grafo de NetworkX solo para visualización
        G = nx.DiGraph()
        G.add_node(nodo)
        
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
        
        # Limpiar y dibujar
        self.ax.clear()
        
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, ax=self.ax, 
                              node_color='lightblue', 
                              node_size=500,
                              nodelist=[n for n in G.nodes() if n != nodo])
        nx.draw_networkx_nodes(G, pos, ax=self.ax, 
                              node_color='red', 
                              node_size=800,
                              nodelist=[nodo])
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, ax=self.ax, 
                              edge_color='gray', 
                              alpha=0.5,
                              arrows=True,
                              arrowsize=10)
        
        # Etiquetas
        nx.draw_networkx_labels(G, pos, ax=self.ax, 
                               font_size=8)
        
        self.ax.set_title(f'Nodo Crítico: {nodo} ({len(vecinos)} vecinos mostrados)', 
                         fontsize=12, fontweight='bold')
        self.ax.set_axis_off()
        
        self.canvas.draw()
    
    def ejecutar_bfs(self):
        """Ejecutar BFS y visualizar resultado"""
        if not self.grafo:
            messagebox.showwarning("Advertencia", 
                                  "Primero debes cargar un dataset")
            return
        
        try:
            nodo_inicio = int(self.entry_nodo.get())
            profundidad = int(self.entry_prof.get())
            
            if profundidad > 5:
                if not messagebox.askyesno("Advertencia", 
                    "Profundidad > 5 puede generar muchos nodos. ¿Continuar?"):
                    return
            
            self.log(f"🔍 Ejecutando BFS desde nodo {nodo_inicio}, "
                    f"profundidad {profundidad}...")
            
            inicio = time.time()
            nodos, aristas = self.grafo.bfs(nodo_inicio, profundidad)
            fin = time.time()
            
            tiempo = (fin - inicio) * 1000  # En milisegundos
            
            self.log(f"✅ BFS completado en {tiempo:.2f} ms")
            self.log(f"   Nodos encontrados: {len(nodos)}")
            self.log(f"   Aristas: {len(aristas)}")
            
            # Visualizar
            self.visualizar_bfs(nodos, aristas, nodo_inicio)
            
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.log(f"❌ Error: {str(e)}")
    
    def visualizar_bfs(self, nodos, aristas, inicio):
        """Visualizar resultado de BFS"""
        # Limitar visualización
        MAX_NODOS = 200
        
        if len(nodos) > MAX_NODOS:
            self.log(f"⚠️  Limitando visualización a {MAX_NODOS} nodos")
            # Mantener nodo inicial y primeros MAX_NODOS
            nodos_viz = set([inicio] + nodos[1:MAX_NODOS])
            aristas_viz = [(o, d) for o, d in aristas 
                          if o in nodos_viz and d in nodos_viz]
        else:
            nodos_viz = set(nodos)
            aristas_viz = aristas
        
        # Crear grafo de NetworkX
        G = nx.DiGraph()
        G.add_nodes_from(nodos_viz)
        G.add_edges_from(aristas_viz)
        
        # Limpiar y dibujar
        self.ax.clear()
        
        # Layout jerárquico si es pequeño, sino spring
        if len(nodos_viz) < 50:
            try:
                pos = nx.kamada_kawai_layout(G)
            except:
                pos = nx.spring_layout(G, k=0.5, iterations=50)
        else:
            pos = nx.spring_layout(G, k=0.3, iterations=30)
        
        # Colorear por distancia desde inicio
        colores = []
        for nodo in G.nodes():
            if nodo == inicio:
                colores.append('red')
            else:
                colores.append('lightblue')
        
        # Dibujar
        nx.draw_networkx_nodes(G, pos, ax=self.ax, 
                              node_color=colores, 
                              node_size=300)
        nx.draw_networkx_edges(G, pos, ax=self.ax, 
                              edge_color='gray', 
                              alpha=0.3,
                              arrows=True,
                              arrowsize=8)
        
        if len(nodos_viz) < 100:
            nx.draw_networkx_labels(G, pos, ax=self.ax, 
                                   font_size=7)
        
        self.ax.set_title(f'BFS desde Nodo {inicio} - '
                         f'{len(nodos)} nodos, {len(aristas)} aristas', 
                         fontsize=12, fontweight='bold')
        self.ax.set_axis_off()
        
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()