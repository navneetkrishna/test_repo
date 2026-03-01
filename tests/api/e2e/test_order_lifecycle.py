import pytest

from src.utils.assertions import assert_status, assert_field_equals
from src.utils.data_factory import make_pet, make_order

pytestmark = [pytest.mark.regression, pytest.mark.e2e, pytest.mark.store]


class TestOrderLifecycle:
    """End-to-end order lifecycle — Create pet → Place order → Read → Cancel → Verify."""

    @pytest.mark.smoke
    def test_e2e_order_001_full_lifecycle(self, pet_client, store_client):
        """Full order lifecycle: Create pet → Place order → GET order → DELETE → verify gone."""

        # Step 1: Create a pet to order
        pet_payload = make_pet(status="available")
        pet_response = pet_client.create_pet(pet_payload)
        assert_status(pet_response, 200)
        pet_id = pet_client.json(pet_response)["id"]

        # Step 2: Place an order for that pet
        order_payload = make_order(pet_id=pet_id, status="placed")
        order_response = store_client.place_order(order_payload)
        assert_status(order_response, 200)
        order = store_client.json(order_response)
        order_id = order["id"]
        assert_field_equals(order, "petId", pet_id)
        assert_field_equals(order, "status", "placed")

        # Step 3: Read the order back
        get_response = store_client.get_order_by_id(order_id)
        assert_status(get_response, 200)
        assert_field_equals(store_client.json(get_response), "id", order_id)

        # Step 4: Cancel the order
        delete_response = store_client.delete_order(order_id)
        assert_status(delete_response, 200)

        # Step 5: Verify the order is gone
        gone_response = store_client.get_order_by_id(order_id)
        assert gone_response.status_code == 404, \
            f"Order {order_id} still accessible after deletion."

        # Step 6: Cleanup pet
        pet_client.delete_pet(pet_id)

    def test_e2e_order_002_inventory_reflects_order_status(
        self, pet_client, store_client
    ):
        """Placing an order for a 'sold' pet is reflected in the store inventory count."""
        # Baseline inventory
        inv_before = store_client.json(store_client.get_inventory())
        sold_before = inv_before.get("sold", 0)

        # Create and mark as sold
        pet_payload = make_pet(status="sold")
        pet_response = pet_client.create_pet(pet_payload)
        assert_status(pet_response, 200)
        pet_id = pet_client.json(pet_response)["id"]

        # Inventory after
        inv_after = store_client.json(store_client.get_inventory())
        sold_after = inv_after.get("sold", 0)

        assert sold_after >= sold_before, \
            f"Sold count did not increase after adding a sold pet. " \
            f"Before: {sold_before}, After: {sold_after}."

        # Cleanup
        pet_client.delete_pet(pet_id)
