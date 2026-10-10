# Task Service

Microservicio FastAPI que expone operaciones para crear, listar, consultar, modificar y eliminar tareas.

## Ejecutar localmente

Desde la raíz del repositorio, con el entorno Python activado:

```bash
pip install -r services/task-service/requirements.txt
uvicorn app.main:app --reload --app-dir services/task-service --port 8001
```

La documentación interactiva se encuentra en `http://127.0.0.1:8001/docs` y el endpoint de salud en `http://127.0.0.1:8001/health`.

## Endpoints

| Método | Ruta | Operación |
| --- | --- | --- |
| `POST` | `/tasks` | Crear una tarea |
| `GET` | `/tasks` | Listar tareas |
| `GET` | `/tasks/{task_id}` | Consultar una tarea |
| `PATCH` | `/tasks/{task_id}` | Modificar campos de una tarea |
| `DELETE` | `/tasks/{task_id}` | Eliminar una tarea |

Por ahora los registros viven en memoria y se pierden al reiniciar el servicio. El almacenamiento SQLite corresponde al issue B10.

## Valores permitidos

- Estado: `Pendiente`, `En proceso` o `Terminada`.
- Prioridad: `Baja`, `Media` o `Alta`.
- Si no se especifican, una tarea nueva inicia como `Pendiente` y con prioridad `Media`.
- Un estado o prioridad fuera de esas opciones se rechaza con `422 Unprocessable Entity` tanto al crear como al modificar una tarea.
