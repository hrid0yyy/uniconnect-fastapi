from fastapi import FastAPI
from .middleware.auth_middleware import verify_server_token
from .routers import inference

app = FastAPI()

app.middleware("http")(verify_server_token)
app.include_router(inference.router)

@app.get("/")
def read_root():
    return {"message": "Therap BD - FastAPI"}


