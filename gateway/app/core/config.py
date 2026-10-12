import os


def _frontend_origins() -> list[str]:
    configured_origins = os.getenv("FRONTEND_ORIGINS")
    if not configured_origins:
        return ["http://localhost:5173", "http://127.0.0.1:5173"]
    return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]


class Settings:
    api_prefix = "/api"
    frontend_origins = _frontend_origins()
    task_service_url = os.getenv("TASK_SERVICE_URL", "http://127.0.0.1:8001").rstrip("/")
    member_service_url = os.getenv("MEMBER_SERVICE_URL", "http://127.0.0.1:8002").rstrip("/")
    service_timeout_seconds = float(os.getenv("SERVICE_TIMEOUT_SECONDS", "5"))


settings = Settings()
