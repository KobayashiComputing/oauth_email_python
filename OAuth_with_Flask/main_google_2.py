from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

app = Flask(__name__)

# Replace with your Google OAuth 2.0 Client ID
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

def verify_google_id_token(token):
    """
    Verifies a Google ID token and returns the decoded user info.
    Raises ValueError if the token is invalid.
    """
    try:
        # Verify token with Google's public keys
        id_info = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Optional: Ensure token is from accounts.google.com
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Wrong issuer.")

        return id_info  # Contains 'sub', 'email', 'name', etc.

    except ValueError as e:
        # Token is invalid or expired
        raise ValueError(f"Invalid token: {e}")

@app.route("/auth/google", methods=["POST"])
def google_auth():
    """
    Endpoint to verify Google ID token sent from frontend.
    Expects JSON: { "id_token": "<token>" }
    """
    data = request.get_json()
    if not data or "id_token" not in data:
        return jsonify({"error": "Missing id_token"}), 400

    token = data["id_token"]

    try:
        user_info = verify_google_id_token(token)
        return jsonify({
            "status": "success",
            "user_id": user_info["sub"],  # Unique Google user ID
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(debug=True)
