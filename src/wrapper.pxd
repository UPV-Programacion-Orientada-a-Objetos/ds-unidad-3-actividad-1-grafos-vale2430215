# distutils: language = c++

cdef extern from "grafo.h":
    cdef cppclass GrafoBase:
        pass
    
    cdef struct ResultadoBFS:
        int* nodos
        int* aristas_origen
        int* aristas_destino
        int num_nodos
        int num_aristas
    
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        bint cargarDatos(const char* archivo)
        int obtenerGrado(int nodo)
        int* getVecinos(int nodo, int& count)
        ResultadoBFS BFS(int inicio, int profundidad)
        int obtenerNumNodos()
        int obtenerNumAristas()
        int encontrarNodoMaxGrado()