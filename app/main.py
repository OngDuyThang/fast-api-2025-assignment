from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import auth, company, task, user
from starlette import status

app = FastAPI()

for module in [auth, user, company, task]:
    app.include_router(module.router)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "Ok"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation Error", "message": exception.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exception):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": "HTTP Request Error", "message": str(exception)},
    )


@app.exception_handler(Exception)
async def database_exception_handler(_, exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error", "message": str(exception)},
    )
