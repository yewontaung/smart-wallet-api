from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import ResourceNotFoundException


def handle_resource_not_found_exception(request:Request, e:ResourceNotFoundException):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "message": e.message,
        },
    )