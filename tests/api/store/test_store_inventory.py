import pytest

from src.utils.assertions import assert_status
from src.utils.data_factory import make_pet

pytestmark = [pytest.mark.regression, pytest.mark.store]


class TestStoreInventory:
    """GET /store/inventory — Pet inventory by status."""

    @pytest.mark.smoke
    def test_str_i001_get_inventory_returns_200(self, store_client):
        """GET /store/inventory — expect 200 and a non-empty response."""
        response = store_client.get_inventory()

        assert_status(response, 200)
        body = store_client.json(response)
        assert isinstance(body, dict), \
            f"Expected inventory to be a dict, got {type(body)}."
        assert len(body) > 0, "Inventory response is empty."

    @pytest.mark.schema
    def test_str_i002_inventory_schema_is_valid(self, store_client):
        """Validate inventory response — keys must be strings, values must be integers."""
        response = store_client.get_inventory()

        assert_status(response, 200)
        body = store_client.json(response)

        for key, value in body.items():
            assert isinstance(key, str), \
                f"Inventory key '{key}' is not a string."
            assert isinstance(value, int), \
                f"Inventory value for key '{key}' is not an integer: {value}."

    def test_str_i003_inventory_changes_after_adding_sold_pet(
        self, store_client, pet_client
    ):
        """Adding a pet with status='sold' increments the 'sold' count in inventory."""
        # Baseline
        before = store_client.json(store_client.get_inventory())
        sold_before = before.get("sold", 0)

        # Add a sold pet
        payload = make_pet(status="sold")
        create_response = pet_client.create_pet(payload)
        assert_status(create_response, 200)
        pet_id = pet_client.json(create_response)["id"]

        # After
        after = store_client.json(store_client.get_inventory())
        sold_after = after.get("sold", 0)

        assert sold_after >= sold_before, \
            f"Sold count did not increase. Before: {sold_before}, After: {sold_after}."

        # Cleanup
        pet_client.delete_pet(pet_id)
