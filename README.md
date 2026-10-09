# FlowJob

FlowJob es una aplicación web para organizar las tareas de un equipo de trabajo. Permite registrar, consultar, modificar y eliminar tareas, asignarlas a integrantes, definir su prioridad y dar seguimiento a su estado.

El proyecto se desarrollará como una aplicación distribuida siguiendo una arquitectura de microservicios. React proporciona la interfaz; un API Gateway recibe las solicitudes del frontend y las dirige a los servicios de backend desarrollados con FastAPI. Cada servicio administra sus propios datos mediante una base SQLite independiente.

## Funcionalidades previstas

- Crear, consultar, editar y eliminar tareas.
- Asignar tareas a integrantes del equipo.
- Cambiar el estado de una tarea: Pendiente, En proceso o Terminada.
- Establecer prioridad: Baja, Media o Alta.
- Filtrar tareas por estado y responsable.

## Integrantes

Completar con los nombres de todas las personas del equipo:

| Integrante | Usuario de Git |
| --- | --- |
| Avril Alexa | Just-Seven y Just-Quackss |
| Guadalupe Jáquez | Delulw |
| Adán Ramirez | JustPolar1 |

## Tecnologías

- **Frontend:** React y Vite.
- **API Gateway:** FastAPI.
- **Servicios backend:** FastAPI.
- **Persistencia:** SQLite, con una base de datos propiedad de cada servicio.
- **Control de versiones:** Git y GitHub.

## Arquitectura y organización

```text
frontend/                    # Interfaz React/Vite
  src/
    features/                 # Funcionalidades de la interfaz
    services/                 # Cliente HTTP hacia el Gateway
gateway/                     # API Gateway FastAPI
  app/
    api/routes/               # Rutas públicas y health check
    clients/                  # Clientes HTTP hacia los microservicios
services/
  task-service/               # Gestión de tareas y su base SQLite
    app/
      api/routes/
      core/
      db/
      models/
      schemas/
      services/
  member-service/             # Gestión de integrantes y su base SQLite
    app/                       # Misma separación interna que task-service
docs/                         # Arquitectura, APIs, datos y acuerdos del equipo
```

Cada servicio es responsable de su lógica y de sus datos. Los servicios no consultan directamente las bases de datos de otros servicios; la comunicación se realiza mediante sus APIs. El Gateway ofrece al frontend un punto de entrada común.

## Requisitos

- Python 3.12 o compatible con las dependencias del proyecto.
- Node.js y npm.
- Git.

## Ejecución local

La estructura inicial contiene las aplicaciones y endpoints de salud. Las funciones de tareas, integrantes y persistencia se agregarán en los siguientes cambios.

1. Clonar el repositorio y entrar al proyecto:

   ```bash
   git clone https://github.com/JustPolar1/FlowJob.git
   cd FlowJob
   ```

2. Crear y activar un entorno Python e instalar las dependencias (desde la raíz):

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r gateway/requirements.txt
   pip install -r services/task-service/requirements.txt
   pip install -r services/member-service/requirements.txt
   ```

3. Iniciar el Gateway y cada microservicio en terminales separadas, manteniendo activo el entorno virtual:

   ```bash
   uvicorn app.main:app --reload --app-dir gateway --port 8000
   uvicorn app.main:app --reload --app-dir services/task-service --port 8001
   uvicorn app.main:app --reload --app-dir services/member-service --port 8002
   ```

   Cada servicio expone actualmente `/health`. La documentación interactiva de FastAPI está en `/docs` de cada puerto, por ejemplo `http://127.0.0.1:8000/docs`.

4. En otra terminal, iniciar React:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Abrir la dirección local que muestre Vite (configurada por defecto en `http://localhost:5173`). Las solicitudes bajo `/api` están preparadas para dirigirse al Gateway; las rutas funcionales se agregarán después.

## Documentación

La documentación técnica y los acuerdos del equipo se mantendrán en [`docs/`](docs/). Documentos disponibles:

- [Flujo de trabajo y reglas de colaboración](docs/flujo-de-trabajo.md): ramas, commits, Pull/Merge Requests, revisión e integración.
- [Arquitectura inicial](docs/arquitectura.md): responsabilidades de componentes, estructura interna y propiedad de datos.

Se agregarán aquí enlaces al modelo de datos y documentación de endpoints conforme se elaboren.

## Estado del proyecto

En preparación. La estructura y los comandos de ejecución de esta guía son la propuesta inicial y deberán mantenerse alineados con la implementación real.
