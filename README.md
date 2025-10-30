# Sistema de Creación de DataSets a través de la Transcripción de Videos

## 🚀 Visión General del Proyecto

Este proyecto tiene como objetivo principal desarrollar un sistema robusto para la creación automatizada de datasets a partir de la transcripción de contenido de video. La idea es facilitar la generación de conjuntos de datos estructurados que puedan ser utilizados para diversas aplicaciones, como el entrenamiento de modelos de Machine Learning, análisis de contenido, o búsqueda avanzada.

Actualmente, estamos en una fase de avance significativa, con la configuración base del backend y la infraestructura de la API ya establecidas.

## ✨ Estado Actual del Avance

Hasta la fecha, se ha logrado lo siguiente:

- **Configuración del Proyecto Django:** La estructura principal del proyecto Django (`trans_project`) está configurada y funcionando.
- **API RESTful:** Se ha integrado Django REST Framework (`rest_framework`) para construir una API RESTful, que será el punto de comunicación principal para interactuar con el sistema (por ejemplo, para subir videos, gestionar transcripciones y generar datasets).
- **Gestión de Medios:** El sistema está configurado para manejar y servir archivos multimedia (videos, etc.) a través de `MEDIA_URL` y `MEDIA_ROOT`, lo que es fundamental para el almacenamiento de los videos a procesar.
- **Base de Datos MySQL:** Se ha configurado la conexión con una base de datos MySQL (`tcp_videos`), que almacenará toda la información relevante del proyecto, incluyendo metadatos de videos, transcripciones y detalles de los datasets generados.
- **CORS Habilitado:** Se ha implementado `django-cors-headers` con `CORS_ALLOW_ALL_ORIGINS = True`, permitiendo la comunicación sin restricciones con clientes frontend desde cualquier origen durante la fase de desarrollo.
- **Aplicación `api`:** Se ha creado y registrado la aplicación `api` dentro del proyecto, que contendrá la lógica específica para la gestión de videos, transcripciones y la generación de datasets. Sus URLs ya están incluidas en el proyecto principal.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.x, Django
- **API:** Django REST Framework
- **Base de Datos:** MySQL
- **Manejo de CORS:** `django-cors-headers`

## ⚙️ Configuración y Ejecución (para desarrollo)

Para poner en marcha el proyecto localmente:

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd tns_videos_datasets/backend
    ```
2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate     # En Windows
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt # (Asumiendo que existe un requirements.txt)
    # Si no existe, instalar manualmente:
    # pip install Django djangorestframework mysqlclient django-cors-headers
    ```
4.  **Configurar la base de datos:** Asegúrate de que tu servidor MySQL esté corriendo y que la base de datos `tcp_videos` exista, o créala.
5.  **Realizar migraciones:**
    ```bash
    python manage.py migrate
    ```
6.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    El servidor estará disponible en `http://127.0.0.1:8000/`.

## ➡️ Próximos Pasos

Los siguientes pasos en el desarrollo incluyen:

- Definir los modelos de datos para videos, transcripciones y datasets.
- Implementar los `Serializers` y `Views` en la aplicación `api` para la gestión de recursos.
- Integrar una librería o servicio de transcripción de audio/video.
- Desarrollar la lógica para procesar videos, generar transcripciones y estructurar los datasets.
