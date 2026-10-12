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

El Member Service administra su propia SQLite en `services/member-service/data/members.db` (configurable con `MEMBER_DATABASE_URL`) y crea al iniciar la tabla `members`, que contiene un identificador y un nombre. El servicio permite registrar y consultar integrantes mediante su API HTTP. El Task Service administra `services/task-service/data/tasks.db` (configurable con `TASK_DATABASE_URL`) y crea la tabla `tasks`, con título, descripción opcional, identificador de responsable, estado, prioridad y fechas. Las bases son independientes; la validación de responsables se realiza mediante API, no con una clave foránea entre archivos SQLite.

El Task Service permite asignar un integrante mediante `assignee_id` al crear una tarea (`POST /tasks`) o actualizarla (`PATCH /tasks/{task_id}`). El identificador se guarda y se devuelve en la respuesta; además, el servicio comprueba que el integrante exista en el Member Service antes de guardar la asignación. El Gateway publica `GET`, `POST` y `PATCH` de tareas bajo `/api/tasks` y consulta los integrantes en `/api/members`. La URL del Task Service se configura con `TASK_SERVICE_URL` (por defecto `http://127.0.0.1:8001`) y la del Member Service con `MEMBER_SERVICE_URL` (por defecto `http://127.0.0.1:8002`). La interfaz permite crear y editar tareas desde su página.
