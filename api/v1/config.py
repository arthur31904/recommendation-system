from schemas.response import SuccessResponse, ErrorResponse


Responses = {
    200: {"model": SuccessResponse},
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}
