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
frontend/                   # Interfaz React; se comunica con el Gateway
gateway/                    # API Gateway FastAPI
services/
  task-service/              # Gestión de tareas y su base SQLite
  member-service/            # Gestión de integrantes y su base SQLite
docs/                        # Arquitectura, APIs, datos y acuerdos del equipo
```

Cada servicio es responsable de su lógica y de sus datos. Los servicios no consultan directamente las bases de datos de otros servicios; la comunicación se realiza mediante sus APIs. El Gateway ofrece al frontend un punto de entrada común.

## Requisitos

- Python 3.12 o compatible con las dependencias del proyecto.
- Node.js y npm.
- Git.

## Ejecución local

...

## Documentación

La documentación técnica y los acuerdos del equipo se mantendrán en [`docs/`](docs/). Documentos disponibles:

- [Flujo de trabajo y reglas de colaboración](docs/flujo-de-trabajo.md): ramas, commits, Pull/Merge Requests, revisión e integración.

Se agregarán aquí enlaces al diagrama de arquitectura, responsabilidades de cada servicio, modelo de datos y documentación de endpoints conforme se elaboren.

## Estado del proyecto

En preparación. La estructura y los comandos de ejecución de esta guía son la propuesta inicial y deberán mantenerse alineados con la implementación real.
