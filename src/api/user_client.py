from requests import Response

from src.api.base_client import BaseClient


class UserClient(BaseClient):
    """API client for the /user domain.

    Endpoint reference:
        POST   /user                     — Create a new user
        POST   /user/createWithArray     — Create users from an array
        POST   /user/createWithList      — Create users from a list
        GET    /user/login               — Log user into the system
        GET    /user/logout              — Log out current user
        GET    /user/{username}          — Get user by username
        PUT    /user/{username}          — Update user
        DELETE /user/{username}          — Delete user
    """

    _BASE = "/user"

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_user(self, payload: dict) -> Response:
        """POST /user — Create a single user."""
        return self.post(self._BASE, json=payload)

    def create_users_with_list(self, payloads: list[dict]) -> Response:
        """POST /user/createWithList — Create multiple users at once."""
        return self.post(f"{self._BASE}/createWithList", json=payloads)

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username: str, password: str) -> Response:
        """GET /user/login — Log in and receive a session token."""
        return self.get(f"{self._BASE}/login", params={
            "username": username,
            "password": password
        })

    def logout(self) -> Response:
        """GET /user/logout — Log out the current session."""
        return self.get(f"{self._BASE}/logout")

    # ------------------------------------------------------------------
    # Read / Update / Delete
    # ------------------------------------------------------------------

    def get_user(self, username: str) -> Response:
        """GET /user/{username} — Retrieve a user by username."""
        return self.get(f"{self._BASE}/{username}")

    def update_user(self, username: str, payload: dict) -> Response:
        """PUT /user/{username} — Update a user's details."""
        return self.put(f"{self._BASE}/{username}", json=payload)

    def delete_user(self, username: str) -> Response:
        """DELETE /user/{username} — Delete a user."""
        return self.delete(f"{self._BASE}/{username}")
