import pytest

from src.api.pet_client import PetClient
from src.api.store_client import StoreClient
from src.api.user_client import UserClient
from src.utils.data_factory import make_pet, make_order, make_user


# ------------------------------------------------------------------
# API client fixtures  (session-scoped — one instance for the full run)
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def pet_client() -> PetClient:
    """Shared PetClient instance for the entire test session."""
    return PetClient()


@pytest.fixture(scope="session")
def store_client() -> StoreClient:
    """Shared StoreClient instance for the entire test session."""
    return StoreClient()


@pytest.fixture(scope="session")
def user_client() -> UserClient:
    """Shared UserClient instance for the entire test session."""
    return UserClient()


# ------------------------------------------------------------------
# Resource fixtures — create once, clean up after each test
# ------------------------------------------------------------------

@pytest.fixture(scope="function")
def created_pet(pet_client):
    """Create a fresh 'available' pet before a test and delete it after.

    Yields the full response body dict so tests can read any field.
    """
    payload = make_pet(status="available")
    response = pet_client.create_pet(payload)
    assert response.status_code == 200, \
        f"[Fixture] Failed to create pet. Status: {response.status_code}, Body: {response.text}"

    pet = response.json()
    yield pet

    # Teardown — best-effort delete; ignore 404 if already deleted by the test
    pet_client.delete_pet(pet["id"])


@pytest.fixture(scope="function")
def created_order(pet_client, store_client, created_pet):
    """Place a fresh order for the created_pet and delete it after.

    Depends on created_pet so the pet always exists before the order is placed.
    Yields the full order response body dict.
    """
    payload = make_order(pet_id=created_pet["id"])
    response = store_client.place_order(payload)
    assert response.status_code == 200, \
        f"[Fixture] Failed to place order. Status: {response.status_code}, Body: {response.text}"

    order = response.json()
    yield order

    # Teardown
    store_client.delete_order(order["id"])


@pytest.fixture(scope="function")
def created_user(user_client):
    """Create a fresh user before a test and delete it after.

    Yields the original payload dict (Petstore's POST /user only returns
    a message, not the full user object).
    """
    payload = make_user()
    response = user_client.create_user(payload)
    assert response.status_code == 200, \
        f"[Fixture] Failed to create user. Status: {response.status_code}, Body: {response.text}"

    yield payload

    # Teardown
    user_client.delete_user(payload["username"])
