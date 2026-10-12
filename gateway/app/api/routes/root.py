from fastapi import APIRouter

router = APIRouter()


@router.get("", summary="Gateway API information")
def api_information() -> dict[str, str]:
    return {
        "service": "flowjob-api-gateway",
        "version": "0.1.0",
        "status": "ready",
    }
