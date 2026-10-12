import httpx
from fastapi import HTTPException, Request
from fastapi.responses import Response

from app.core.config import settings


async def forward_request(
    request: Request,
    *,
    service_name: str,
    service_url: str,
    service_path: str,
) -> Response:
    """Forward an HTTP request and preserve the downstream response."""
    url = f"{service_url.rstrip('/')}/{service_path.lstrip('/')}"
    forwarded_headers = {
        name: value
        for name, value in request.headers.items()
        if name.lower() in {"accept", "authorization", "content-type"}
    }

    try:
        async with httpx.AsyncClient(timeout=settings.service_timeout_seconds) as client:
            upstream_response = await client.request(
                method=request.method,
                url=url,
                params=request.query_params.multi_items(),
                headers=forwarded_headers,
                content=await request.body(),
            )
    except httpx.TimeoutException as error:
        raise HTTPException(
            status_code=504,
            detail={
                "service": service_name,
                "message": "El servicio tardó demasiado en responder.",
            },
        ) from error
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "service": service_name,
                "message": "El servicio no está disponible.",
            },
        ) from error

    response_headers = {
        name: value
        for name, value in upstream_response.headers.items()
        if name.lower() in {"content-type", "location", "www-authenticate", "retry-after"}
    }
    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
    )
