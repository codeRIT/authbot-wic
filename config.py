
from typing import List
from dotenv import load_dotenv
import os

load_dotenv(override=True)

PREFIX: str = "/"
REGISTRATION_ROLE: str = "Hackers"

AUTH_TOKEN: str = os.getenv("AUTH_TOKEN")
AUTH_URL: str = os.getenv("AUTH_URL")

# client things are from HM
CLIENT_ID: str = os.getenv("CLIENT_ID")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")

REDIRECT_URI: str = os.getenv("REDIRECT_URI")
OAUTH_SCOPES: List[str] = ["main"]

APPLY_URL: str = "https://apply.wichacks.io/"

HOST: str = os.getenv("HOST", "localhost")
PORT: str = os.getenv("PORT", 8080)
