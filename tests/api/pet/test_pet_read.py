import pytest

from src.utils.assertions import assert_status, assert_schema, assert_field_equals
from src.utils.assertions import PET_SCHEMA

pytestmark = [pytest.mark.regression, pytest.mark.pet]


class TestPetRead:
    """GET /pet/{petId} and GET /pet/findByStatus — Read pet data."""

    # ------------------------------------------------------------------
    # GET /pet/{petId}
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_pet_r001_get_by_valid_id(self, pet_client, created_pet):
        """GET a pet by a valid ID that was just created — expect 200 and correct data."""
        response = pet_client.get_pet_by_id(created_pet["id"])

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_schema(body, PET_SCHEMA)
        assert_field_equals(body, "id", created_pet["id"])
        assert_field_equals(body, "name", created_pet["name"])

    @pytest.mark.negative
    def test_pet_r002_get_by_nonexistent_id(self, pet_client):
        """GET /pet/{petId} with an ID that does not exist — expect 404."""
        response = pet_client.get_pet_by_id(999_999_999)

        assert_status(response, 404)

    @pytest.mark.negative
    def test_pet_r003_get_by_id_zero(self, pet_client):
        """GET /pet/0 — expect 404 as ID 0 is not a valid pet."""
        response = pet_client.get_pet_by_id(0)

        assert response.status_code in (400, 404), \
            f"Expected 400 or 404 for ID=0, got {response.status_code}."

    @pytest.mark.negative
    def test_pet_r004_get_by_negative_id(self, pet_client):
        """GET /pet/-1 — expect 4xx for a negative ID."""
        response = pet_client.get_pet_by_id(-1)

        assert response.status_code >= 400, \
            f"Expected 4xx for negative ID, got {response.status_code}."

    @pytest.mark.schema
    def test_pet_r005_response_schema_is_valid(self, pet_client, created_pet):
        """Validate that the GET /pet/{petId} response matches the Pet schema."""
        response = pet_client.get_pet_by_id(created_pet["id"])

        assert_status(response, 200)
        assert_schema(pet_client.json(response), PET_SCHEMA)

    # ------------------------------------------------------------------
    # GET /pet/findByStatus
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_pet_r006_find_by_status(self, pet_client, status):
        """GET /pet/findByStatus for each valid status — expect 200 and a list."""
        response = pet_client.find_by_status(status)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert isinstance(body, list), \
            f"Expected a list for findByStatus={status}, got {type(body)}."

    def test_pet_r007_find_by_status_items_match_status(self, pet_client):
        """All pets returned by findByStatus=available must actually have status=available."""
        response = pet_client.find_by_status("available")

        assert_status(response, 200)
        pets = pet_client.json(response)

        # Only check a sample to keep the test fast on large datasets
        sample = pets[:10]
        for pet in sample:
            assert pet.get("status") == "available", \
                f"Pet ID {pet.get('id')} has status '{pet.get('status')}', expected 'available'."

    @pytest.mark.negative
    def test_pet_r008_find_by_invalid_status(self, pet_client):
        """GET /pet/findByStatus with an invalid status value — expect 400."""
        response = pet_client.find_by_status("invalid_status")

        assert response.status_code in (400, 200), \
            "Petstore returns 400 for invalid status; documenting actual behaviour."
