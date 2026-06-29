import secrets

from flask import (
    Blueprint,
    current_app,
    make_response,
    redirect,
    request,
    session,
    url_for,
)

from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/oauth/login')
def login():
    # Generate a CSRF state token and remember it for the callback (step 1)
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    return redirect(AuthService.build_authorize_url(state))


@auth_bp.route('/oauth/callback')
def callback():
    # APS redirects the user back here with ?code= and ?state= (step 2)
    error = request.args.get('error')
    if error:
        description = request.args.get('error_description', '')
        return f"Authorization failed: {error} - {description}", 400

    state = request.args.get('state')
    if not state or state != session.pop('oauth_state', None):
        return "Invalid state parameter. Possible CSRF attempt.", 400

    code = request.args.get('code')
    if not code:
        return "No authorization code returned.", 400

    # Exchange the code for an access token (step 3)
    token = AuthService.exchange_code(code)
    session['access_token'] = token.get('access_token')
    session['refresh_token'] = token.get('refresh_token')

    profile = AuthService.get_user_profile(token.get('access_token'))
    if profile:
        session['user_name'] = profile.get('name') or profile.get('email')

    return redirect(url_for('main.index'))


@auth_bp.route('/oauth/logout')
def logout():
    # Drop the server-side session contents...
    session.clear()
    # ...and explicitly expire the session cookie in the browser.
    response = make_response(redirect(url_for('main.index')))
    response.delete_cookie(
        current_app.config.get('SESSION_COOKIE_NAME', 'session'),
        path=current_app.config.get('SESSION_COOKIE_PATH') or '/',
        domain=current_app.config.get('SESSION_COOKIE_DOMAIN'),
    )
    return response
