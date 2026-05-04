# 🧬 Validador de Secuencias Biológicas

Herramienta completa para **validando ORFs (Open Reading Frames)** en secuencias de ADN utilizando algoritmos avanzados de búsqueda de patrones y autómatas finitos deterministas. Incluye tanto una interfaz web interactiva como herramientas de línea de comandos.

**Repositorio:** [github.com/LeonardoEspinoza7373/Validador-de-Secuencias-Biologicas](https://github.com/LeonardoEspinoza7373/Validador-de-Secuencias-Biologicas)

## ✨ Características Principales

- **Validando ORFs**: Aplicando todas las reglas biológicas para verificar secuencias de ADN
- **Buscando KMP**: Algoritmo eficiente de búsqueda de patrones (codones)
- **Simulando AFD**: Visualizando el recorrido del autómata finito determinista
- **Interfaz Web**: Aplicación Flask moderna y responsiva
- **Entrada Dual**: Cargando archivos FASTA o ingresando secuencias manualmente
- **API REST**: Endpoints para validación programática
- **Mostrando Resultados**: Información completa sobre cada secuencia validada
- **Filtrando Avanzados**: Filtrando resultados entre secuencias válidas e inválidas
- **Exportando**: Copiando secuencias al portapapeles

## 📋 Requisitos del Sistema

- **Python**: 3.7 o superior
- **Flask**: 2.3.2+
- **Navegador Moderno**: Para la interfaz web

## 🚀 Instalación Rápida

### 1. Clonando el repositorio

```bash
git clone https://github.com/LeonardoEspinoza7373/Validador-de-Secuencias-Biologicas.git
cd Validador-de-Secuencias-Biologicas
```

### 2. Creando entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalando dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutando la aplicación web

```bash
cd frontend
python3 app_web.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📖 Guía de Uso

### 🌐 Interfaz Web (Recomendado)

#### Opción 1: Cargando Archivo FASTA

1. Abriendo http://localhost:5000 en tu navegador
2. Haciendo clic en la pestaña **"📁 Cargando Archivo FASTA"**
3. Arrastrando un archivo `.fasta` o haciendo clic para seleccionar
4. Haciendo clic en **"Validando Secuencias"**
5. Explorando los resultados:
   - Filtrando entre válidas e inválidas
   - Haciendo clic en **"Ver detalles"** para información completa
   - Copiando secuencias al portapapeles

#### Opción 2: Ingresando Secuencia Manual

1. Haciendo clic en la pestaña **"✏️ Ingresando Secuencia"**
2. Ingresando un nombre para la secuencia (ej: ORF_001)
3. Pegando o escribiendo la secuencia de ADN
4. La aplicación validando en tiempo real los caracteres
5. Haciendo clic en **"Validando Secuencia"**
6. Visualizando los resultados instantáneamente

### 💻 Línea de Comandos

Validando archivos desde terminal:

```bash
python3 main.py
```

Editando `main.py` para cambiar la ruta del archivo:

```python
RUTA_ARCHIVO_FASTA = "/path/to/tu_archivo.fasta"
```

## 📁 Formateando Archivo FASTA

El formato FASTA requiere:
- Línea de descripción que comienza con `>`
- Una o más líneas de secuencia
- Solo caracteres A, T, G, C válidos

**Ejemplo:**

```fasta
>ORF_valida
ATGAAATAA

>ORF_sin_stop
ATGAAA

>ORF_invalida_caracteres
ATGAAATAX
```

## 🧪 Utilizando Archivo de Ejemplo

El proyecto incluye `secuencias.fasta` con ejemplos de secuencias válidas e inválidas.

## 🔍 Reglas de Validación

Una ORF es válida si cumple con **TODAS** estas condiciones:

| Regla | Descripción | Validación |
|-------|-------------|-----------|
| **Alfabeto** | Solo caracteres A, C, G, T | ✓ Requerido |
| **Inicio** | Comenzando con ATG | ✓ Requerido |
| **Longitud mínima** | Mínimo 6 nucleótidos | ✓ ATG + Stop |
| **Marco de lectura** | Longitud múltiplo de 3 | ✓ Requerido |
| **Parada** | Terminando con TAA, TAG o TGA | ✓ Requerido |
| **Sin stops internos** | Sin codones stop en el marco | ✓ Requerido |
| **AFD** | Aceptada por el autómata | ✓ Requerido |

## 🏗️ Estructura del Proyecto

```
Validador-de-Secuencias-Biologicas/
├── 📄 README.md                          # Este archivo
├── 📄 FRONTEND_README.md                 # Documentación del frontend
├── 📄 QUICK_START.md                     # Guía rápida
├── 📦 requirements.txt                   # Dependencias Python
├── 📄 main.py                            # Script CLI
├── 📄 secuencias.fasta                   # Archivo de ejemplo
│
├── 🔧 Módulos Core
│   ├── afd.py                            # Simulación del AFD
│   ├── kmp.py                            # Algoritmo KMP
│   ├── lector_fasta.py                   # Lector de archivos FASTA
│   ├── modelos.py                        # Estructuras de datos
│   └── orf.py                            # Lógica de validación
│
├── 🌐 Frontend (Web)
│   └── frontend/
│       ├── app_web.py                    # Servidor Flask
│       ├── templates/
│       │   └── index.html                # Interfaz web
│       └── static/
│           ├── css/
│           │   └── estilos.css           # Estilos CSS
│           └── js/
│               └── validador.js          # Lógica frontend
│
└── 🔐 Entorno Virtual
    └── venv/                             # Dependencias instaladas
```

## 🔌 API REST

### Endpoint 1: Validando Archivo FASTA

**Solicitud:**
```http
POST /api/validar
Content-Type: multipart/form-data

archivo: [archivo FASTA]
```

**Respuesta:**
```json
{
  "exito": true,
  "total_registros": 3,
  "total_validas": 1,
  "resultados": [
    {
      "nombre_registro": "ORF_valida",
      "secuencia": "ATGAAATAA",
      "es_valida": true,
      "motivo": "ORF válida.",
      "coincidencias": {
        "posiciones_atg": [0],
        "posiciones_taa": [6],
        "posiciones_tag": [],
        "posiciones_tga": []
      },
      "recorrido_afd": {
        "aceptada": true,
        "estado_final": "aceptacion",
        "estados_visitados": ["inicial", "..."]
      }
    }
  ]
}
```

### Endpoint 2: Validando Secuencia Individual

**Solicitud:**
```http
POST /api/validar-secuencia
Content-Type: application/json

{
  "nombre": "mi_orf",
  "secuencia": "ATGAAATAA"
}
```

**Respuesta:**
```json
{
  "exito": true,
  "resultado": {
    "nombre_registro": "mi_orf",
    "secuencia": "ATGAAATAA",
    "es_valida": true,
    "motivo": "ORF válida.",
    "coincidencias": {...},
    "recorrido_afd": {...}
  }
}
```

## 🧩 Componentes Técnicos

### Algoritmo KMP (Knuth-Morris-Pratt)

- **Complejidad**: O(n + m)
- **Uso**: Buscando eficientemente codones (ATG, TAA, TAG, TGA)
- **Ventaja**: No requiriendo backtracking

### Autómata Finito Determinista (AFD)

- **Estados**: Estado inicial, transiciones según secuencia
- **Aceptación**: Verificando estructura general de la ORF
- **Recorrido**: Registrando cada transición de estado

### Modelos de Datos

```python
@dataclass
class RegistroFasta:
    nombre: str
    secuencia: str

@dataclass
class ResultadoValidacion:
    nombre_registro: str
    secuencia: str
    es_valida: bool
    motivo: str
    coincidencias: CoincidenciasPatrones
    recorrido_afd: RecorridoMaquina
```

## 🎨 Interfaz Web

### Características Visuales

- **Diseño Responsivo**: Compatible con móviles, tablets y desktop
- **Tema Moderno**: Utilizando gradientes, animaciones suaves y colores profesionales
- **Modo Oscuro**: Interfaz adaptable al tema del sistema
- **Accesibilidad**: Etiquetas semánticas y navegación intuitiva

### Tecnologías Frontend

- HTML5 semántico
- CSS3 con variables personalizables
- JavaScript vanilla (sin dependencias)
- Fetch API para comunicación con backend

## 🔧 Configurando Avanzadamente

### Cambiando Puerto

En `frontend/app_web.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Cambiar puerto aquí
```

### Personalizando Colores

En `frontend/static/css/estilos.css`:

```css
:root {
    --color-primario: #2ecc71;      /* Verde */
    --color-secundario: #3498db;    /* Azul */
    --color-error: #e74c3c;         /* Rojo */
    --color-advertencia: #f39c12;   /* Naranja */
}
```

### Desactivando Modo Debug

```python
app.run(debug=False, port=5000)
```

## 📊 Ejemplos de Uso

### Ejemplo 1: ORF Válida

**Entrada:**
```
Nombre: ORF_001
Secuencia: ATGAAATAA
```

**Resultado:**
- ✅ Válida
- Motivo: "ORF válida."
- ATG en: [0]
- TAA en: [6]

### Ejemplo 2: ORF Sin Codón Stop

**Entrada:**
```
Nombre: ORF_incompleta
Secuencia: ATGAAA
```

**Resultado:**
- ❌ Inválida
- Motivo: "Secuencia incompleta: no alcanza para codón de inicio y codón stop."

### Ejemplo 3: Marco de Lectura Incorrecto

**Entrada:**
```
Nombre: ORF_marco_incorrecto
Secuencia: ATGAAATA
```

**Resultado:**
- ❌ Inválida
- Motivo: "No respeta el marco de lectura: la longitud no es múltiplo de 3."

## 🐛 Solucionando Problemas

| Problema | Solución |
|----------|----------|
| **"Port already in use"** | Ejecutando `lsof -i :5000` y luego `kill -9 <PID>` |
| **"No module named 'flask'"** | Instalando `pip install -r requirements.txt` |
| **"ModuleNotFoundError"** | Asegurándote que estés en el directorio correcto |
| **Archivo FASTA no encontrado** | Verificando la ruta absoluta en `main.py` |
| **Caracteres inválidos** | Escribiendo la secuencia con solo A, T, G, C |
| **Servidor no responde** | Reiniciando con `Ctrl+C` y `python3 app_web.py` |

## 📚 Referencias Externas

- [FASTA Format](https://en.wikipedia.org/wiki/FASTA_format)
- [Open Reading Frame](https://en.wikipedia.org/wiki/Open_reading_frame)
- [Algoritmo KMP](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
- [Autómatas Finitos Deterministas](https://en.wikipedia.org/wiki/Deterministic_finite_automaton)
- [Bioinformática](https://en.wikipedia.org/wiki/Bioinformatics)

## 🚀 Mejorando en el Futuro

- [ ] Soportando archivos FASTQ
- [ ] Analizando múltiples frames
- [ ] Visualizando gráficamente alineamientos
- [ ] Exportando a formatos adicionales (CSV, JSON)
- [ ] Validando proteínas traducidas
- [ ] Buscando motivos comunes
- [ ] Calculando estadísticas de composición GC
- [ ] Almacenando caché de resultados

## 📝 Licencia

Proyecto educativo - Bioinformática y Teoría de Autómatas

Libre para uso académico y no comercial.

## 👤 Autor

Desarrollado por **Leonardo Espinoza** como proyecto educativo de Teoría de Autómatas y Bioinformática.

**Repositorio**: [github.com/LeonardoEspinoza7373/Validador-de-Secuencias-Biologicas](https://github.com/LeonardoEspinoza7373/Validador-de-Secuencias-Biologicas)

## 💬 Soporte

Para reportando problemas o sugerencias, abriendo un issue en el repositorio.

---

**Versión**: 1.0  
**Última actualización**: Mayo 3, 2026  
**Estado**: ✅ Funcional y operando correctamente
