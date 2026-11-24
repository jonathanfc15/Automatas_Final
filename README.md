# Lumo — Editor de Código y Compilador

Entorno de desarrollo y compilador diseñado para el lenguaje de programación **Lumo**, implementado en Python con interfaz gráfica en **Qt6 (PySide6)** y motor de análisis léxico/sintáctico construido con **PLY**.

## Características principales
- **Editor de texto completo:** Crear, abrir, guardar archivos, copiar, cortar, pegar y búsqueda de texto en tiempo real.
- **Análisis Léxico y Sintáctico:** Visualización detallada de la tabla de **Tokens**, árbol **AST**, reporte de **Errores** y **Salida** de ejecución.

## Requisitos e instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/jonathanfc15/Autómatas_Final.git
   cd Autómatas_Final
   
## Arquitectura del Compilador Lumo

El flujo de compilación y ejecución dentro del paquete `compiler/` consta de cuatro etapas:

1. **Análisis Léxico (`compiler/lexer.py`):** Tokeniza el código fuente identificando palabras reservadas (`ent`, `dec`, `txt`, `bool`, `simon`, `nosimon`, `mientras`, `funchion`, `retorno`, `muestrame`, `verdad`, `falso`, `Y`, `O`, `NONES`), literales, identificadores y operadores.
2. **Análisis Sintáctico (`compiler/parser.py`):** Construye el Árbol de Sintaxis Abstracta (AST) verificando la estructura gramatical y la precedencia de operadores.
3. **Análisis Semántico (`compiler/semantic.py`):** Valida tipos de datos, declaración previa de variables y correspondencia de argumentos en llamadas a funciones.
4. **Intérprete (`compiler/interpreter.py`):** Recorre el AST validado para ejecutar las instrucciones y mostrar la salida de `muestrame(...)` en la consola de la interfaz.

## Atajos de Teclado del Editor (`app.py`)

| Atajo | Acción |
|---|---|
| `Ctrl + N` | Crear un nuevo archivo en el editor |
| `Ctrl + O` | Abrir archivo fuente (`.lumo` / `.ism`) |
| `Ctrl + S` | Guardar el archivo activo |
| `Ctrl + F` | Enfocar la barra de búsqueda en el editor |
| `F5` | Compilar y ejecutar el código fuente |

## Pruebas Automatizadas

Para validar por consola el funcionamiento del analizador léxico y sintáctico sobre todos los casos de prueba ubicados en `examples/`:

```bash
python tests/test_compilador.py