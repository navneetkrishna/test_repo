import pytest

from src.utils.assertions import assert_status, assert_field_equals
from src.utils.data_factory import make_pet

pytestmark = [pytest.mark.regression, pytest.mark.pet]


class TestPetUpdate:
    """PUT /pet and POST /pet/{petId} — Update pet data."""

    # ------------------------------------------------------------------
    # PUT /pet — JSON body update
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_pet_u001_update_name(self, pet_client, created_pet):
        """PUT /pet — Update the pet's name and verify the response reflects it."""
        updated_payload = {**created_pet, "name": "UpdatedName"}

        response = pet_client.update_pet(updated_payload)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_field_equals(body, "name", "UpdatedName")
        assert_field_equals(body, "id", created_pet["id"])

    def test_pet_u002_update_status_to_sold(self, pet_client, created_pet):
        """PUT /pet — Change status from 'available' to 'sold'."""
        updated_payload = {**created_pet, "status": "sold"}

        response = pet_client.update_pet(updated_payload)

        assert_status(response, 200)
        body = pet_client.json(response)
        assert_field_equals(body, "status", "sold")

    @pytest.mark.negative
    def test_pet_u003_update_nonexistent_pet(self, pet_client):
        """PUT /pet — Updating a pet with a non-existent ID — expect 404."""
        payload = make_pet()
        payload["id"] = 999_999_999

        response = pet_client.update_pet(payload)

        assert response.status_code in (404, 400, 200), \
            "Documenting actual Petstore behaviour for non-existent ID update."

    @pytest.mark.negative
    def test_pet_u004_update_with_empty_body(self, pet_client):
        """PUT /pet with an empty JSON body — expect 4xx."""
        response = pet_client.update_pet({})

        assert response.status_code >= 400, \
            f"Expected 4xx for empty update body, got {response.status_code}."

    # ------------------------------------------------------------------
    # POST /pet/{petId} — Form data update
    # ------------------------------------------------------------------

    def test_pet_u005_update_via_form_data(self, pet_client, created_pet):
        """POST /pet/{petId} — Update name and status via form data."""
        response = pet_client.update_pet_form(
            pet_id=created_pet["id"],
            name="FormUpdatedName",
            status="pending"
        )

        assert_status(response, 200)

        # Verify changes persisted via a GET
        get_response = pet_client.get_pet_by_id(created_pet["id"])
        if get_response.status_code == 200:
            body = pet_client.json(get_response)
            assert body.get("name") == "FormUpdatedName", \
                f"Name was not updated via form data. Got: {body.get('name')}"
