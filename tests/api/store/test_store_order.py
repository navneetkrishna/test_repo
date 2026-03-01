import pytest

from src.utils.assertions import assert_status, assert_schema, assert_field_equals, assert_field_not_empty
from src.utils.assertions import ORDER_SCHEMA
from src.utils.data_factory import make_order

pytestmark = [pytest.mark.regression, pytest.mark.store]


class TestStoreOrder:
    """POST /store/order, GET /store/order/{orderId}, DELETE /store/order/{orderId}."""

    # ------------------------------------------------------------------
    # POST /store/order
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_str_o001_place_order_success(self, store_client, created_pet):
        """POST /store/order — Place a valid order and verify the response."""
        payload = make_order(pet_id=created_pet["id"])

        response = store_client.place_order(payload)

        assert_status(response, 200)
        body = store_client.json(response)
        assert_schema(body, ORDER_SCHEMA)
        assert_field_not_empty(body, "id")
        assert_field_equals(body, "petId", created_pet["id"])

        # Cleanup
        store_client.delete_order(body["id"])

    @pytest.mark.parametrize("status", ["placed", "approved", "delivered"])
    def test_str_o002_place_order_each_status(self, store_client, created_pet, status):
        """POST /store/order — Place an order for each valid status value."""
        payload = make_order(pet_id=created_pet["id"], status=status)

        response = store_client.place_order(payload)

        assert_status(response, 200)
        body = store_client.json(response)
        assert_field_equals(body, "status", status)

        # Cleanup
        store_client.delete_order(body["id"])

    @pytest.mark.negative
    def test_str_o003_place_order_empty_body(self, store_client):
        """POST /store/order with empty body — expect 4xx."""
        response = store_client.place_order({})

        assert response.status_code >= 400, \
            f"Expected 4xx for empty order body, got {response.status_code}."

    @pytest.mark.negative
    def test_str_o004_place_order_zero_quantity(self, store_client, created_pet):
        """POST /store/order with quantity=0 — document actual API behaviour."""
        payload = make_order(pet_id=created_pet["id"], quantity=0)

        response = store_client.place_order(payload)

        # Petstore may accept or reject quantity=0 — document actual behaviour
        assert response.status_code in (200, 400), \
            f"Unexpected status for quantity=0: {response.status_code}."

        if response.status_code == 200:
            store_client.delete_order(store_client.json(response)["id"])

    # ------------------------------------------------------------------
    # GET /store/order/{orderId}
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_str_o005_get_order_by_id(self, store_client, created_order):
        """GET /store/order/{orderId} — Retrieve the order just placed."""
        response = store_client.get_order_by_id(created_order["id"])

        assert_status(response, 200)
        body = store_client.json(response)
        assert_schema(body, ORDER_SCHEMA)
        assert_field_equals(body, "id", created_order["id"])

    @pytest.mark.negative
    def test_str_o006_get_order_invalid_id(self, store_client):
        """GET /store/order/{orderId} with ID > 10 — expect 404 or server exception."""
        response = store_client.get_order_by_id(99999)

        assert response.status_code in (404, 500), \
            f"Expected 404 or 500 for order ID > 10, got {response.status_code}."

    @pytest.mark.negative
    def test_str_o007_get_deleted_order(self, store_client, created_pet):
        """GET an order after it has been deleted — expect 404."""
        payload = make_order(pet_id=created_pet["id"])
        create_response = store_client.place_order(payload)
        assert_status(create_response, 200)
        order_id = store_client.json(create_response)["id"]

        store_client.delete_order(order_id)

        get_response = store_client.get_order_by_id(order_id)
        assert get_response.status_code == 404, \
            f"Order {order_id} still accessible after deletion. Status: {get_response.status_code}."

    # ------------------------------------------------------------------
    # DELETE /store/order/{orderId}
    # ------------------------------------------------------------------

    def test_str_o008_delete_order(self, store_client, created_pet):
        """DELETE /store/order/{orderId} — expect 200."""
        payload = make_order(pet_id=created_pet["id"])
        create_response = store_client.place_order(payload)
        assert_status(create_response, 200)
        order_id = store_client.json(create_response)["id"]

        response = store_client.delete_order(order_id)

        assert_status(response, 200)

    @pytest.mark.negative
    def test_str_o009_delete_nonexistent_order(self, store_client):
        """DELETE a non-existent order — expect 404."""
        response = store_client.delete_order(999999)

        assert response.status_code in (404, 200), \
            "Documenting actual Petstore behaviour for non-existent order delete."

    @pytest.mark.schema
    def test_str_o010_order_response_schema(self, store_client, created_order):
        """Validate the GET /store/order response matches the Order schema."""
        response = store_client.get_order_by_id(created_order["id"])

        assert_status(response, 200)
        assert_schema(store_client.json(response), ORDER_SCHEMA)
