from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.auth_middleware import verify_server_token
from src.routers import inference, notes, agent
from src.utils.generate_test_token import generate_test_token
from src.config import cloudinary_config 

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Disable auth middleware for development purposes
#app.middleware("http")(verify_server_token)
#generate_test_token()

app.include_router(inference.router)
app.include_router(notes.router)
app.include_router(agent.router)
  

@app.get("/")
def read_root():
    return {"message": "Therap BD - FastAPI"}


