import base64
from urllib.parse import urlencode

import requests
from flask import current_app


class AuthService:
    """Implements the APS 3-legged OAuth (Authorization Code) flow."""

    @staticmethod
    def build_authorize_url(state):
        """Build the APS authorize URL the user is redirected to (step 1)."""
        params = {
            'response_type': 'code',
            'client_id': current_app.config['APS_CLIENT_ID'],
            'redirect_uri': current_app.config['APS_REDIRECT_URI'],
            'scope': current_app.config['APS_SCOPE'],
            'state': state,
        }
        return f"{current_app.config['APS_AUTHORIZE_URL']}?{urlencode(params)}"

    @staticmethod
    def exchange_code(code):
        """Exchange the authorization code for an access token (step 3)."""
        client_id = current_app.config['APS_CLIENT_ID']
        client_secret = current_app.config['APS_CLIENT_SECRET']
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

        headers = {
            'Authorization': f'Basic {basic}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': current_app.config['APS_REDIRECT_URI'],
        }
        response = requests.post(
            current_app.config['APS_TOKEN_URL'],
            headers=headers,
            data=data,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_user_profile(access_token):
        """Fetch the signed-in user's profile (requires user-profile:read scope)."""
        response = requests.get(
            current_app.config['APS_USERINFO_URL'],
            headers={'Authorization': f'Bearer {access_token}'},
        )
        if response.status_code == 200:
            return response.json()
        return None
