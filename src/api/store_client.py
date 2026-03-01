from requests import Response

from src.api.base_client import BaseClient


class StoreClient(BaseClient):
    """API client for the /store domain.

    Endpoint reference:
        GET    /store/inventory          — Returns pet inventories by status
        POST   /store/order              — Place an order for a pet
        GET    /store/order/{orderId}    — Find purchase order by ID
        DELETE /store/order/{orderId}    — Delete purchase order by ID
    """

    _BASE = "/store"

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def get_inventory(self) -> Response:
        """GET /store/inventory — Returns a map of status → count."""
        return self.get(f"{self._BASE}/inventory")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def place_order(self, payload: dict) -> Response:
        """POST /store/order — Place a new order."""
        return self.post(f"{self._BASE}/order", json=payload)

    def get_order_by_id(self, order_id: int) -> Response:
        """GET /store/order/{orderId} — Retrieve an order.

        Note: Petstore only supports order IDs 1–10 reliably.
        IDs > 10 may raise a server-side exception.
        """
        return self.get(f"{self._BASE}/order/{order_id}")

    def delete_order(self, order_id: int) -> Response:
        """DELETE /store/order/{orderId} — Cancel and delete an order."""
        return self.delete(f"{self._BASE}/order/{order_id}")
