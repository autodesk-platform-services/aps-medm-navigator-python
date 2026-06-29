from flask import Blueprint, render_template, jsonify, session

from app.services.medm_service import MEDMService

api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template(
        'index.html',
        authenticated='access_token' in session,
        user_name=session.get('user_name'),
    )

@api_bp.before_request
def require_auth():
    if 'access_token' not in session:
        return jsonify({'error': 'not_authenticated'}), 401

@api_bp.route('/collections')
def collections():
    return jsonify(MEDMService.get_collections())

@api_bp.route('/collections/<collection_id>/projects')
def projects(collection_id):
    return jsonify(MEDMService.get_projects(collection_id))

@api_bp.route('/projects/<project_id>/assets')
def assets(project_id):
    return jsonify(MEDMService.get_assets(project_id))
