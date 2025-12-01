#include "grafo.h"

// Constructor
GrafoDisperso::GrafoDisperso() {
    num_nodos = 0;
    num_aristas = 0;
    capacidad_nodos = 1000;
    capacidad_aristas = 10000;
    
    // Asignación manual de memoria
    row_ptr = (int*)malloc(sizeof(int) * (capacidad_nodos + 1));
    col_indices = (int*)malloc(sizeof(int) * capacidad_aristas);
    
    if (!row_ptr || !col_indices) {
        std::cerr << "[Error] No se pudo asignar memoria inicial" << std::endl;
        exit(1);
    }
    
    row_ptr[0] = 0;
}

// Destructor
GrafoDisperso::~GrafoDisperso() {
    free(row_ptr);
    free(col_indices);
}

// Expandir capacidad de nodos
void GrafoDisperso::expandirNodos() {
    capacidad_nodos *= 2;
    int* nuevo_ptr = (int*)realloc(row_ptr, sizeof(int) * (capacidad_nodos + 1));
    if (!nuevo_ptr) {
        std::cerr << "[Error] No se pudo expandir row_ptr" << std::endl;
        exit(1);
    }
    row_ptr = nuevo_ptr;
}

// Expandir capacidad de aristas
void GrafoDisperso::expandirAristas() {
    capacidad_aristas *= 2;
    int* nuevo_col = (int*)realloc(col_indices, sizeof(int) * capacidad_aristas);
    if (!nuevo_col) {
        std::cerr << "[Error] No se pudo expandir col_indices" << std::endl;
        exit(1);
    }
    col_indices = nuevo_col;
}

// Cargar datos desde archivo formato Edge List
bool GrafoDisperso::cargarDatos(const char* archivo) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "[Error] No se pudo abrir el archivo" << std::endl;
        return false;
    }
    
    // Estructuras temporales para construir el grafo
    int* temp_origen = (int*)malloc(sizeof(int) * 1000000);
    int* temp_destino = (int*)malloc(sizeof(int) * 1000000);
    int temp_count = 0;
    int temp_capacity = 1000000;
    int max_nodo = 0;
    
    // Leer todas las aristas
    char linea[256];
    while (file.getline(linea, 256)) {
        // Saltar comentarios
        if (linea[0] == '#') continue;
        
        int origen, destino;
        if (sscanf(linea, "%d %d", &origen, &destino) == 2) {
            if (temp_count >= temp_capacity) {
                temp_capacity *= 2;
                temp_origen = (int*)realloc(temp_origen, sizeof(int) * temp_capacity);
                temp_destino = (int*)realloc(temp_destino, sizeof(int) * temp_capacity);
            }
            
            temp_origen[temp_count] = origen;
            temp_destino[temp_count] = destino;
            temp_count++;
            
            if (origen > max_nodo) max_nodo = origen;
            if (destino > max_nodo) max_nodo = destino;
        }
    }
    file.close();
    
    num_nodos = max_nodo + 1;
    num_aristas = temp_count;
    
    // Asegurar capacidad suficiente
    while (num_nodos > capacidad_nodos) expandirNodos();
    while (num_aristas > capacidad_aristas) expandirAristas();
    
    // Contar grados de salida de cada nodo
    int* grados = (int*)calloc(num_nodos, sizeof(int));
    for (int i = 0; i < num_aristas; i++) {
        grados[temp_origen[i]]++;
    }
    
    // Construir row_ptr (CSR)
    row_ptr[0] = 0;
    for (int i = 0; i < num_nodos; i++) {
        row_ptr[i + 1] = row_ptr[i] + grados[i];
    }
    
    // Resetear grados para usarlos como índices temporales
    memset(grados, 0, sizeof(int) * num_nodos);
    
    // Llenar col_indices
    for (int i = 0; i < num_aristas; i++) {
        int origen = temp_origen[i];
        int destino = temp_destino[i];
        int pos = row_ptr[origen] + grados[origen];
        col_indices[pos] = destino;
        grados[origen]++;
    }
    
    // Liberar memoria temporal
    free(temp_origen);
    free(temp_destino);
    free(grados);
    
    // Calcular memoria estimada
    int memoria_mb = ((num_nodos + 1) * sizeof(int) + num_aristas * sizeof(int)) / (1024 * 1024);
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos 
              << " | Aristas: " << num_aristas << std::endl;
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " 
              << memoria_mb << " MB." << std::endl;
    
    return true;
}

// Obtener grado de un nodo (número de vecinos)
int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo < 0 || nodo >= num_nodos) return 0;
    return row_ptr[nodo + 1] - row_ptr[nodo];
}

// Obtener vecinos de un nodo
int* GrafoDisperso::getVecinos(int nodo, int& count) {
    if (nodo < 0 || nodo >= num_nodos) {
        count = 0;
        return nullptr;
    }
    
    int inicio = row_ptr[nodo];
    int fin = row_ptr[nodo + 1];
    count = fin - inicio;
    
    if (count == 0) return nullptr;
    
    int* vecinos = (int*)malloc(sizeof(int) * count);
    for (int i = 0; i < count; i++) {
        vecinos[i] = col_indices[inicio + i];
    }
    
    return vecinos;
}

// Encontrar nodo con mayor grado
int GrafoDisperso::encontrarNodoMaxGrado() {
    int max_grado = 0;
    int nodo_max = 0;
    
    for (int i = 0; i < num_nodos; i++) {
        int grado = obtenerGrado(i);
        if (grado > max_grado) {
            max_grado = grado;
            nodo_max = i;
        }
    }
    
    std::cout << "[C++ Core] Nodo con mayor grado: " << nodo_max 
              << " (Grado: " << max_grado << ")" << std::endl;
    
    return nodo_max;
}

// BFS implementado manualmente
ResultadoBFS GrafoDisperso::BFS(int inicio, int profundidad) {
    std::cout << "[C++ Core] Ejecutando BFS desde Nodo " << inicio 
              << ", Profundidad " << profundidad << std::endl;
    
    ResultadoBFS resultado;
    resultado.nodos = nullptr;
    resultado.aristas_origen = nullptr;
    resultado.aristas_destino = nullptr;
    resultado.num_nodos = 0;
    resultado.num_aristas = 0;
    
    if (inicio < 0 || inicio >= num_nodos) {
        std::cerr << "[Error] Nodo inicial fuera de rango" << std::endl;
        return resultado;
    }
    
    // Cola manual usando arreglo circular
    int* cola = (int*)malloc(sizeof(int) * num_nodos);
    int* nivel = (int*)malloc(sizeof(int) * num_nodos);
    bool* visitado = (bool*)calloc(num_nodos, sizeof(bool));
    
    int frente = 0, final = 0;
    
    // Iniciar BFS
    cola[final] = inicio;
    nivel[final] = 0;
    final++;
    visitado[inicio] = true;
    
    // Arreglos temporales para resultados
    int* temp_nodos = (int*)malloc(sizeof(int) * num_nodos);
    int* temp_aristas_o = (int*)malloc(sizeof(int) * num_aristas);
    int* temp_aristas_d = (int*)malloc(sizeof(int) * num_aristas);
    int count_nodos = 0;
    int count_aristas = 0;
    
    temp_nodos[count_nodos++] = inicio;
    
    // Procesar cola
    while (frente < final) {
        int actual = cola[frente];
        int nivel_actual = nivel[frente];
        frente++;
        
        if (nivel_actual >= profundidad) continue;
        
        // Obtener vecinos
        int inicio_vec = row_ptr[actual];
        int fin_vec = row_ptr[actual + 1];
        
        for (int i = inicio_vec; i < fin_vec; i++) {
            int vecino = col_indices[i];
            
            // Agregar arista
            temp_aristas_o[count_aristas] = actual;
            temp_aristas_d[count_aristas] = vecino;
            count_aristas++;
            
            if (!visitado[vecino]) {
                visitado[vecino] = true;
                cola[final] = vecino;
                nivel[final] = nivel_actual + 1;
                final++;
                temp_nodos[count_nodos++] = vecino;
            }
        }
    }
    
    // Copiar resultados
    resultado.num_nodos = count_nodos;
    resultado.num_aristas = count_aristas;
    resultado.nodos = (int*)malloc(sizeof(int) * count_nodos);
    resultado.aristas_origen = (int*)malloc(sizeof(int) * count_aristas);
    resultado.aristas_destino = (int*)malloc(sizeof(int) * count_aristas);
    
    memcpy(resultado.nodos, temp_nodos, sizeof(int) * count_nodos);
    memcpy(resultado.aristas_origen, temp_aristas_o, sizeof(int) * count_aristas);
    memcpy(resultado.aristas_destino, temp_aristas_d, sizeof(int) * count_aristas);
    
    // Liberar memoria temporal
    free(cola);
    free(nivel);
    free(visitado);
    free(temp_nodos);
    free(temp_aristas_o);
    free(temp_aristas_d);
    
    std::cout << "[C++ Core] Nodos encontrados: " << count_nodos << std::endl;
    
    return resultado;
}