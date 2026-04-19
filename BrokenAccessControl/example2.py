# @app.route('/account/<user_id>')
# def get_account(user_id):
#     user = db.query(User).filter_by(id=user_id).first()
#     return jsonify(user.to_dict())
from flask import jsonify, abort
from flask_login import login_required, current_user

@app.route('/account/<int:user_id>')   # enforces type
@login_required                         # rejects unauthenticated requests
def get_account(user_id):
    # authorization
    # admins could be allowed here
    if current_user.id != user_id:
        abort(403)                       
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        abort(404)                       # safe
    return jsonify(user.to_dict()), 200