# API Gateway

FastAPI es el punto de entrada HTTP del frontend. El frontend de Vite envía las solicitudes `/api/*` al Gateway; este servicio centraliza CORS y la configuración de las APIs internas.

## Ejecutar localmente

Desde la raíz del repositorio, con el entorno Python activado:

```bash
pip install -r gateway/requirements.txt
uvicorn app.main:app --reload --app-dir gateway --port 8000
```

- Información del Gateway: `http://127.0.0.1:8000/api`
- Salud del servicio: `http://127.0.0.1:8000/health`
- OpenAPI: `http://127.0.0.1:8000/docs`

## Configuración

El Gateway admite estas variables de entorno:

| Variable | Valor local predeterminado | Uso |
| --- | --- | --- |
| `FRONTEND_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Orígenes permitidos por CORS, separados por comas |
| `TASK_SERVICE_URL` | `http://127.0.0.1:8001` | Dirección interna del servicio de tareas |
| `MEMBER_SERVICE_URL` | `http://127.0.0.1:8002` | Dirección interna del servicio de integrantes |

Las rutas que reenvían solicitudes a cada servicio se añadirán en sus issues correspondientes (B15 y B16).
