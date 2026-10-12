from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.core.config import settings
from app.core.proxy import forward_request


router = APIRouter(prefix="/members")
MEMBER_METHODS = ["GET", "POST"]


@router.api_route("", methods=MEMBER_METHODS, summary="Forward member collection requests")
async def member_collection(request: Request) -> Response:
    return await forward_request(
        request,
        service_name="member-service",
        service_url=settings.member_service_url,
        service_path="members",
    )


@router.api_route(
    "/{path:path}",
    methods=MEMBER_METHODS,
    summary="Forward member resource requests",
)
async def member_resource(path: str, request: Request) -> Response:
    return await forward_request(
        request,
        service_name="member-service",
        service_url=settings.member_service_url,
        service_path=f"members/{path}",
    )
