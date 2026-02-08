"""
Simple authentication for FastHTML Gantt Chart app.

Uses environment variables for username/password.
Session-based - stays logged in until logout.
"""

import os
import hashlib
from fasthtml.common import *

# Default credentials (override with environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
# For security, hash the password
ADMIN_PASSWORD_HASH = hashlib.sha256(
    os.getenv('ADMIN_PASSWORD', 'changeme123').encode()
).hexdigest()


def hash_password(password):
    """Hash a password for storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(username, password):
    """Verify username and password."""
    if username != ADMIN_USERNAME:
        return False
    
    password_hash = hash_password(password)
    return password_hash == ADMIN_PASSWORD_HASH


def is_authenticated(request):
    """Check if user is authenticated via session."""
    session = request.session
    return session.get('authenticated', False)


def login_page(error=None):
    """Generate login page HTML."""
    return Title("Login - Gantt Chart"), Main(
        Div(
            Div(
                H1("🔒 Gantt Chart Manager"),
                P("Please log in to access your projects", style="color: #666; margin-bottom: 30px;"),
                
                Form(
                    Div(
                        Label("Username"),
                        Input(
                            type="text",
                            name="username",
                            placeholder="Enter username",
                            required=True,
                            autofocus=True,
                            style="width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px;"
                        ),
                    ),
                    Div(
                        Label("Password"),
                        Input(
                            type="password",
                            name="password",
                            placeholder="Enter password",
                            required=True,
                            style="width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px;"
                        ),
                    ),
                    Button(
                        "Login",
                        type="submit",
                        style="width: 100%; padding: 12px; background: #4CAF50; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"
                    ),
                    P(error, style="color: #f44336; margin-top: 15px; text-align: center;") if error else "",
                    method="post",
                    action="/login"
                ),
                
                Div(
                    P("Default credentials:", style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;"),
                    P(f"Username: {ADMIN_USERNAME}", style="color: #999; font-size: 12px; margin: 5px 0;"),
                    P("Password: (set via ADMIN_PASSWORD env var)", style="color: #999; font-size: 12px; margin: 5px 0;"),
                    style="text-align: center;"
                ),
                
                style="background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; width: 100%;"
            ),
            style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; padding: 20px;"
        )
    )


def logout_button():
    """Generate logout button for navbar."""
    return Div(
        Form(
            Button(
                "🚪 Logout",
                type="submit",
                style="background: #f44336; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 14px;"
            ),
            method="post",
            action="/logout",
            style="display: inline-block; margin-bottom: 20px;"
        ),
        style="text-align: right; margin-bottom: 10px;"
    )
