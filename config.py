import os
from dotenv import load_dotenv

# Load values from the .env file in the project root
load_dotenv()

class Config:
    GRAPHQL_URL = "https://developer.api.autodesk.com/medm/v2/graphql"

    # APS OAuth (3-legged) credentials, loaded from .env
    APS_CLIENT_ID = os.getenv('APS_CLIENT_ID')
    APS_CLIENT_SECRET = os.getenv('APS_CLIENT_SECRET')
    APS_REDIRECT_URI = os.getenv('APS_REDIRECT_URI', 'http://localhost:5000/oauth/callback')
    APS_SCOPE = os.getenv('APS_SCOPE', 'user-profile:read')

    # APS Authentication v2 endpoints
    # https://aps.autodesk.com/en/docs/oauth/v2/tutorials/get-3-legged-token/
    APS_AUTHORIZE_URL = "https://developer.api.autodesk.com/authentication/v2/authorize"
    APS_TOKEN_URL = "https://developer.api.autodesk.com/authentication/v2/token"
    APS_USERINFO_URL = "https://api.userprofile.autodesk.com/userinfo"

    # Secret key used to sign the session cookie (stores the OAuth state + token)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-only-insecure-key')

    PORT = 5000
    DEBUG = True
