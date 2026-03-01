import pytest

from src.utils.assertions import assert_status, assert_field_equals
from src.utils.data_factory import make_pet

pytestmark = [pytest.mark.regression, pytest.mark.e2e, pytest.mark.pet]


class TestPetLifecycle:
    """End-to-end pet lifecycle — Create → Read → Update → Delete → Verify."""

    @pytest.mark.smoke
    def test_e2e_pet_001_full_lifecycle(self, pet_client):
        """Full pet lifecycle: Create → GET → Update name → Update status → DELETE → verify gone."""

        # Step 1: Create
        payload = make_pet(status="available")
        create_response = pet_client.create_pet(payload)
        assert_status(create_response, 200)
        pet = pet_client.json(create_response)
        pet_id = pet["id"]

        # Step 2: Read — verify it exists
        get_response = pet_client.get_pet_by_id(pet_id)
        assert_status(get_response, 200)
        assert_field_equals(pet_client.json(get_response), "id", pet_id)

        # Step 3: Update name
        updated = {**pet, "name": "LifecycleUpdatedName"}
        update_name_response = pet_client.update_pet(updated)
        assert_status(update_name_response, 200)
        assert_field_equals(pet_client.json(update_name_response), "name", "LifecycleUpdatedName")

        # Step 4: Update status to sold
        updated["status"] = "sold"
        update_status_response = pet_client.update_pet(updated)
        assert_status(update_status_response, 200)
        assert_field_equals(pet_client.json(update_status_response), "status", "sold")

        # Step 5: Verify status change persisted
        verify_response = pet_client.get_pet_by_id(pet_id)
        assert_status(verify_response, 200)
        assert_field_equals(pet_client.json(verify_response), "status", "sold")

        # Step 6: Delete
        delete_response = pet_client.delete_pet(pet_id)
        assert_status(delete_response, 200)

        # Step 7: Verify gone
        gone_response = pet_client.get_pet_by_id(pet_id)
        assert gone_response.status_code == 404, \
            f"Pet {pet_id} should be gone after deletion, got {gone_response.status_code}."

    def test_e2e_pet_002_status_appears_in_find_by_status(self, pet_client):
        """Create a pet with status='pending' and confirm it appears in findByStatus=pending."""
        payload = make_pet(status="pending")
        create_response = pet_client.create_pet(payload)
        assert_status(create_response, 200)
        pet_id = pet_client.json(create_response)["id"]
        pet_name = payload["name"]

        try:
            find_response = pet_client.find_by_status("pending")
            assert_status(find_response, 200)
            pets = pet_client.json(find_response)

            pet_ids = [p["id"] for p in pets]
            assert pet_id in pet_ids, \
                f"Newly created pending pet (ID={pet_id}, name={pet_name}) " \
                f"not found in findByStatus=pending results."
        finally:
            # Always clean up even if assertions fail
            pet_client.delete_pet(pet_id)
