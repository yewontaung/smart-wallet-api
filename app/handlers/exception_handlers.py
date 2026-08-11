from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import BusinessException, InsufficientBalanceException, ResourceNotFoundException, UnauthorizedWalletException


def handle_resource_not_found_exception(request:Request, e:ResourceNotFoundException):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "message": e.message,
        },
    )

def handle_business_exception(request:Request, e:BusinessException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "message": e.message,
        },
    )

def handle_unauthorized_wallet_exception(request:Request, e:UnauthorizedWalletException):
    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={
            "message": e.message,
        },
    )

def handle_insufficient_balance_exception(request:Request, e:InsufficientBalanceException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "message": e.message,
        },
    )
