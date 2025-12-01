#ifndef GRAFO_H
#define GRAFO_H

#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdlib>

// Estructura para almacenar resultados de BFS
struct ResultadoBFS {
    int* nodos;
    int* aristas_origen;
    int* aristas_destino;
    int num_nodos;
    int num_aristas;
};

// Clase Abstracta Base
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual bool cargarDatos(const char* archivo) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual int* getVecinos(int nodo, int& count) = 0;
    virtual ResultadoBFS BFS(int inicio, int profundidad) = 0;
    virtual int obtenerNumNodos() = 0;
    virtual int obtenerNumAristas() = 0;
};

// Clase Concreta con Formato CSR
class GrafoDisperso : public GrafoBase {
private:
    // Formato CSR (Compressed Sparse Row)
    int* row_ptr;        // Punteros de inicio de cada fila
    int* col_indices;    // Índices de columnas
    int num_nodos;
    int num_aristas;
    int capacidad_nodos;
    int capacidad_aristas;
    
    // Método auxiliar para expandir capacidad
    void expandirNodos();
    void expandirAristas();
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    bool cargarDatos(const char* archivo) override;
    int obtenerGrado(int nodo) override;
    int* getVecinos(int nodo, int& count) override;
    ResultadoBFS BFS(int inicio, int profundidad) override;
    int obtenerNumNodos() override { return num_nodos; }
    int obtenerNumAristas() override { return num_aristas; }
    int encontrarNodoMaxGrado();
};

#endif