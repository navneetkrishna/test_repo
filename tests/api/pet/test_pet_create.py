import pytest

from src.utils.assertions import assert_status, assert_schema, assert_field_equals, assert_field_not_empty
from src.utils.assertions import PET_SCHEMA
from src.utils.data_factory import make_pet

pytestmark = [pytest.mark.regression, pytest.mark.pet]


class TestPetCreate:
    """POST /pet — Create a new pet."""

    @pytest.mark.smoke
    def test_pet_c001_create_with_all_fields(self, pet_client):
        """Create a pet with all valid fields — expect 200 and full body returned."""
        payload = make_pet(status="available")

        response = pet_client.create_pet(payload)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_schema(body, PET_SCHEMA)
        assert_field_equals(body, "name", payload["name"])
        assert_field_equals(body, "status", "available")

        # Cleanup
        pet_client.delete_pet(body["id"])

    @pytest.mark.smoke
    def test_pet_c002_create_with_minimum_fields(self, pet_client):
        """Create a pet with only the required fields (name and photoUrls) — expect 200."""
        payload = {
            "name": "MinimalPet",
            "photoUrls": ["https://example.com/photo.jpg"]
        }

        response = pet_client.create_pet(payload)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_field_not_empty(body, "id")
        assert_field_equals(body, "name", "MinimalPet")

        # Cleanup
        pet_client.delete_pet(body["id"])

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_pet_c003_create_with_each_status(self, pet_client, status):
        """Create a pet for each valid status value — expect 200 each time."""
        payload = make_pet(status=status)

        response = pet_client.create_pet(payload)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_field_equals(body, "status", status)

        # Cleanup
        pet_client.delete_pet(body["id"])

    @pytest.mark.negative
    def test_pet_c004_create_with_empty_body(self, pet_client):
        """POST /pet with an empty body — expect a 4xx or 5xx error."""
        response = pet_client.create_pet({})

        assert response.status_code >= 400, \
            f"Expected error status for empty body, got {response.status_code}."

    @pytest.mark.negative
    def test_pet_c005_create_with_invalid_json(self, pet_client):
        """POST /pet with malformed JSON string — expect 4xx."""
        response = pet_client.session.post(
            f"{pet_client.base_url}/pet",
            data="not_valid_json",
            headers={"Content-Type": "application/json"},
            timeout=pet_client.DEFAULT_TIMEOUT
        )

        assert response.status_code in (400, 415, 500), \
            f"Expected 400/415/500 for invalid JSON, got {response.status_code}."
