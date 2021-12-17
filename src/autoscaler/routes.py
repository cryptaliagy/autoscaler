import subprocess

from typing import (
    cast
)

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
)

from cryptography.hazmat.primitives import (
    hashes,
    hmac,
)

from autoscaler.extras import runner

webhook_route = Blueprint('webhook', __name__, url_prefix='/workflows')


@webhook_route.route('heartbeat')
def heartbeat():
    return jsonify(
        ok=True,
        msg='Heartbeat ok!'
    )

@webhook_route.route('/', methods=['POST'])
def created_webhook():
    try:
        gh_token = request.headers['X-Hub-Signature-256'][7:]
        gh_token = bytes.fromhex(gh_token)
    except Exception as e:
        current_app.logger.error(f'Something went wrong: {e}')
        return jsonify(ok=False), 400

    # Github uses HMAC-based auth using a pre-provided secret key
    h = hmac.HMAC(current_app.config['SECRET_TOKEN'].encode(), hashes.SHA256())

    h.update(request.data)

    try:
        h.verify(gh_token)
    except Exception as e:
        current_app.logger.error(f'Failed HMAC authentication: {e}')
        return jsonify(ok=False), 400

    data = cast(dict, request.get_json())

    action = data['action']
    repo = data['repository']['name']
    user = data['repository']['owner']['login']


    current_app.logger.info(f'A job is currently {action} in {user}/{repo}')

    if action == 'completed':
        subprocess.call(['docker', 'container', 'prune', '-f'])
        return jsonify(ok=True), 200

    if action != 'queued':
        return jsonify(ok=True), 200

    try:
        token = runner.create_runner_token(user, repo)
    except ValueError:
        current_app.logger.error('Could not create new token!')
        return jsonify(ok=False), 400

    try:
        subprocess.check_call(
            [
                'docker-compose',
                '-f',
                'devstack/runner.yaml',
                'run',
                '-d',
                '-e',
                f'USER={user}',
                '-e',
                f'REPO={repo}',
                '-e',
                f'TOKEN={token}',
                'runner',
            ]
        )
        return jsonify(ok=True), 200
    except:
        return jsonify(ok=False), 400
