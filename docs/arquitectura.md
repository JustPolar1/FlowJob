# Arquitectura inicial

FlowJob se organiza como una aplicación web con frontend React y servicios independientes construidos con FastAPI. El API Gateway ofrece un punto de entrada HTTP para el frontend y enruta las solicitudes a los servicios de dominio.

## Componentes

| Componente | Responsabilidad | Datos propios |
| --- | --- | --- |
| Frontend React | Presentar tareas e integrantes y capturar acciones del usuario. | Ninguno |
| API Gateway | Recibir llamadas del frontend y dirigirlas a los servicios. | Ninguno |
| Task Service | Reglas y operaciones del ciclo de vida de las tareas. | Base SQLite de tareas |
| Member Service | Registro y consulta de integrantes del equipo. | Base SQLite de integrantes |

## Estructura interna de un servicio

Cada microservicio organiza su código bajo `app/`:

- `api/routes/`: endpoints HTTP.
- `core/`: configuración del servicio.
- `db/`: conexión y configuración de su base SQLite.
- `models/`: modelos de persistencia que pertenecen al servicio.
- `schemas/`: validación de solicitudes y respuestas.
- `services/`: reglas de negocio y coordinación de operaciones propias.

El Gateway contiene `api/routes/` para rutas públicas y `clients/` para la comunicación con los microservicios. El frontend agrupa elementos reutilizables en `components/`, páginas en `pages/`, lógica de interfaz por dominio en `features/` y llamadas HTTP en `services/`.

## Persistencia y comunicación

Cada servicio es dueño de su base SQLite y accede solo a sus propios datos. El Gateway y los demás servicios no consultan directamente esos archivos; la comunicación entre componentes se realiza por HTTP mediante APIs. Las tareas referenciarán al responsable por su identificador, mientras que los datos personales del integrante pertenecen al Member Service.

Esta primera estructura incluye aplicaciones mínimas y endpoints `/health`. Los endpoints del dominio, los modelos de datos, la política de validación de responsables y las rutas del Gateway se definirán e implementarán en las siguientes actividades.

El Task Service permite asignar un integrante mediante `assignee_id` al crear una tarea (`POST /tasks`) o actualizarla (`PATCH /tasks/{task_id}`). El identificador se guarda y se devuelve en la respuesta; la comprobación de que exista en el Member Service queda fuera de esta issue y se atenderá en la issue #12.
