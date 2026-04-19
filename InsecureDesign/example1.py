# @app.route('/reset-password', methods=['POST'])
# def reset_password():
#     email = request.form['email']
#     new_password = request.form['new_password']
#     user = User.query.filter_by(email=email).first()
#     user.password = new_password
#     db.session.commit()
#     return 'Password reset'
import re
import secrets
import bcrypt
from datetime import datetime, timedelta
from flask import request, jsonify
from models import User, db
def is_valid_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None
def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12)
    ).decode("utf-8")
@app.route('/request-reset', methods=['POST'])
def request_reset():
    email = request.form.get('email', '').strip()
    if not email or not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400
    user = User.query.filter_by(email=email).first()
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
        send_reset_email(user.email, token)
    return jsonify({
        "message": "If that email exists, a reset link has been sent."
    }), 200
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.form.get('token', '').strip()
    new_password = request.form.get('new_password', '')
    if not token:
        return jsonify({"error": "Reset token is required"}), 400
    if not new_password or len(new_password) < 12:
        return jsonify({"error": "Password must be at least 12 characters"}), 400
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Token is invalid or has expired"}), 400
    user.password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    return jsonify({"message": "Password successfully reset"}), 200