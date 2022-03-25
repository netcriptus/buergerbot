import os
import secrets

DEBUG = bool(os.getenv("DEBUG", False))
TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = "static"
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(16))
