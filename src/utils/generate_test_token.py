from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def generate_test_token():
    secret_key = os.getenv("SERVER_SECRET_KEY")
    payload = {
        "source": "spring-boot-server"
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("Test Token:", token)

if __name__ == "__main__":
    # To run this script directly, use:
    # python -m src.utils.generate_test_token 
    generate_test_token()