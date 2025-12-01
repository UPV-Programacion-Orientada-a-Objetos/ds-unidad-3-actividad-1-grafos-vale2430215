# distutils: language = c++
# cython: language_level=3

from wrapper cimport GrafoDisperso, ResultadoBFS
from libc.stdlib cimport free

cdef class PyGrafoDisperso:
    cdef GrafoDisperso* grafo
    
    def __cinit__(self):
        self.grafo = new GrafoDisperso()
    
    def __dealloc__(self):
        del self.grafo
    
    def cargar_datos(self, str archivo):
        """Carga un archivo de dataset en formato Edge List"""
        archivo_bytes = archivo.encode('utf-8')
        return self.grafo.cargarDatos(archivo_bytes)
    
    def obtener_grado(self, int nodo):
        """Obtiene el grado (número de conexiones) de un nodo"""
        return self.grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, int nodo):
        """Obtiene la lista de vecinos de un nodo"""
        cdef int count = 0
        cdef int* vecinos = self.grafo.getVecinos(nodo, count)
        
        if vecinos == NULL or count == 0:
            return []
        
        # Convertir a lista de Python
        resultado = [vecinos[i] for i in range(count)]
        free(vecinos)
        
        return resultado
    
    def bfs(self, int inicio, int profundidad):
        """
        Ejecuta BFS desde un nodo con profundidad máxima
        Retorna: (lista_nodos, lista_aristas)
        """
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {inicio}, Profundidad {profundidad}.")
        
        cdef ResultadoBFS resultado = self.grafo.BFS(inicio, profundidad)
        
        # Convertir nodos a lista de Python
        nodos = [resultado.nodos[i] for i in range(resultado.num_nodos)]
        
        # Convertir aristas a lista de tuplas
        aristas = [(resultado.aristas_origen[i], resultado.aristas_destino[i]) 
                   for i in range(resultado.num_aristas)]
        
        # Liberar memoria
        free(resultado.nodos)
        free(resultado.aristas_origen)
        free(resultado.aristas_destino)
        
        print(f"[Cython] Retornando {len(nodos)} nodos y {len(aristas)} aristas a Python.")
        
        return nodos, aristas
    
    def obtener_num_nodos(self):
        """Obtiene el número total de nodos"""
        return self.grafo.obtenerNumNodos()
    
    def obtener_num_aristas(self):
        """Obtiene el número total de aristas"""
        return self.grafo.obtenerNumAristas()
    
    def encontrar_nodo_max_grado(self):
        """Encuentra el nodo con mayor número de conexiones"""
        return self.grafo.encontrarNodoMaxGrado()