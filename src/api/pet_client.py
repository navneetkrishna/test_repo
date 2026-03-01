from requests import Response

from src.api.base_client import BaseClient


class PetClient(BaseClient):
    """API client for the /pet domain.

    Endpoint reference:
        POST   /pet                          — Create a new pet
        PUT    /pet                          — Update an existing pet
        GET    /pet/findByStatus?status=X    — Find pets by status
        GET    /pet/findByTags?tags=X        — Find pets by tags
        GET    /pet/{petId}                  — Get pet by ID
        POST   /pet/{petId}                  — Update pet with form data
        DELETE /pet/{petId}                  — Delete a pet
        POST   /pet/{petId}/uploadFile       — Upload a pet image
    """

    _BASE = "/pet"

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_pet(self, payload: dict) -> Response:
        """POST /pet — Create a new pet."""
        return self.post(self._BASE, json=payload)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_pet_by_id(self, pet_id: int) -> Response:
        """GET /pet/{petId} — Get pet by ID."""
        return self.get(f"{self._BASE}/{pet_id}")

    def find_by_status(self, status: str) -> Response:
        """GET /pet/findByStatus — Find pets by status.

        Args:
            status: One of 'available', 'pending', 'sold'.
        """
        return self.get(f"{self._BASE}/findByStatus", params={"status": status})

    def find_by_tags(self, tags: list[str]) -> Response:
        """GET /pet/findByTags — Find pets by tags."""
        return self.get(f"{self._BASE}/findByTags", params={"tags": tags})

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update_pet(self, payload: dict) -> Response:
        """PUT /pet — Update an existing pet with JSON body."""
        return self.put(self._BASE, json=payload)

    def update_pet_form(self, pet_id: int, name: str = None, status: str = None) -> Response:
        """POST /pet/{petId} — Update pet name and/or status via form data."""
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        # Form data requires overriding Content-Type
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(f"{self._BASE}/{pet_id}", data=data, headers=headers)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_pet(self, pet_id: int) -> Response:
        """DELETE /pet/{petId} — Delete a pet."""
        return self.delete(f"{self._BASE}/{pet_id}")
