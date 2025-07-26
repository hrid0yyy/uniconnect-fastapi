from fastapi import FastAPI
from .middleware.auth_middleware import verify_server_token
from .routers import inference
from .utils.generate_test_token import generate_test_token
app = FastAPI()

app.middleware("http")(verify_server_token)
app.include_router(inference.router)
generate_test_token()
@app.get("/")
def read_root():
    return {"message": "Therap BD - FastAPI"}


