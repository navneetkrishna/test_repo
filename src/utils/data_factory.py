import random
from faker import Faker

fake = Faker()


def make_pet(status: str = "available", pet_id: int = None) -> dict:
    """Generate a valid pet payload.

    Args:
        status: One of 'available', 'pending', 'sold'.
        pet_id: Optional explicit ID. Defaults to a random large int to avoid collisions.

    Returns:
        dict: A pet payload ready for POST /pet or PUT /pet.
    """
    return {
        "id": pet_id or random.randint(100_000, 999_999),
        "category": {
            "id": random.randint(1, 10),
            "name": fake.word().capitalize()
        },
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [
            {"id": random.randint(1, 100), "name": fake.word()}
        ],
        "status": status
    }


def make_order(pet_id: int, quantity: int = 1, status: str = "placed") -> dict:
    """Generate a valid store order payload.

    Args:
        pet_id: ID of the pet being ordered.
        quantity: Number of units.
        status: One of 'placed', 'approved', 'delivered'.

    Returns:
        dict: An order payload ready for POST /store/order.
    """
    return {
        "id": random.randint(1, 10),       # Petstore only accepts IDs 1–10 reliably
        "petId": pet_id,
        "quantity": quantity,
        "shipDate": "2025-01-01T00:00:00.000Z",
        "status": status,
        "complete": False
    }


def make_user(username: str = None) -> dict:
    """Generate a valid user payload.

    Args:
        username: Optional explicit username. Defaults to a unique fake username.

    Returns:
        dict: A user payload ready for POST /user.
    """
    return {
        "id": random.randint(100_000, 999_999),
        "username": username or f"user_{fake.user_name()}_{random.randint(1000, 9999)}",
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
        "phone": fake.phone_number(),
        "userStatus": 1
    }
