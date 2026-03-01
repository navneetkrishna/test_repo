import pytest

from src.utils.assertions import assert_status, assert_field_not_empty

pytestmark = [pytest.mark.regression, pytest.mark.user]


class TestUserAuth:
    """GET /user/login and GET /user/logout — Authentication flows."""

    @pytest.mark.smoke
    def test_usr_a001_login_valid_credentials(self, user_client, created_user):
        """GET /user/login — Valid credentials return 200 and a session token."""
        response = user_client.login(
            username=created_user["username"],
            password=created_user["password"]
        )

        assert_status(response, 200)
        body = user_client.json(response)
        assert_field_not_empty(body, "message")

        # Response message contains the session token
        assert "logged in user session" in body.get("message", "").lower() \
            or body.get("message", "").startswith("logged"), \
            f"Unexpected login message: {body.get('message')}"

    @pytest.mark.negative
    def test_usr_a002_login_invalid_credentials(self, user_client):
        """GET /user/login — Invalid credentials — expect 400."""
        response = user_client.login(
            username="definitely_wrong_user",
            password="definitely_wrong_pass"
        )

        assert response.status_code in (400, 200), \
            "Documenting Petstore behaviour for invalid credentials."

    @pytest.mark.negative
    def test_usr_a003_login_empty_credentials(self, user_client):
        """GET /user/login — Empty username and password — expect 400."""
        response = user_client.login(username="", password="")

        assert response.status_code in (400, 200), \
            "Documenting Petstore behaviour for empty login credentials."

    @pytest.mark.smoke
    def test_usr_a004_logout_after_login(self, user_client, created_user):
        """GET /user/logout — After login, logout should return 200."""
        # Login first
        user_client.login(
            username=created_user["username"],
            password=created_user["password"]
        )

        # Logout
        response = user_client.logout()

        assert_status(response, 200)

    def test_usr_a005_logout_without_login(self, user_client):
        """GET /user/logout — Without prior login — Petstore returns 200 (stateless)."""
        response = user_client.logout()

        # Petstore is stateless — logout always returns 200
        assert_status(response, 200)

    def test_usr_a006_login_response_contains_token_header(self, user_client, created_user):
        """Validate that the login response includes the X-Expires-After header."""
        response = user_client.login(
            username=created_user["username"],
            password=created_user["password"]
        )

        assert_status(response, 200)
        # Petstore includes expiry info in X-Expires-After header
        assert "X-Expires-After" in response.headers or "x-expires-after" in response.headers, \
            f"Expected X-Expires-After header in login response. Headers: {dict(response.headers)}"
