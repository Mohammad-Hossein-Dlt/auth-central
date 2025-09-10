from enum import Enum
from fastapi import FastAPI
from typing import Any

class AppStates(str, Enum):
    AUTH_BASE_URL = "auth_base_url"
    AUTH_DB_CLIENT = "auth_db_client"

def set_app_state(
    app: FastAPI,
    key,
    value: Any,
):
    """Set a state in the FastAPI app."""
    app.state.__setattr__(key, value)


def get_app_state(
    app: FastAPI,
    key,
):
    """Get a state from the FastAPI app."""
    return app.state.__getattr__(key)
