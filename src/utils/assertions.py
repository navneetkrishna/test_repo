import jsonschema

# ------------------------------------------------------------------
# Shared JSON schemas
# ------------------------------------------------------------------

PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls", "status"],
    "properties": {
        "id":        {"type": "integer"},
        "name":      {"type": "string", "minLength": 1},
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "status":    {"type": "string", "enum": ["available", "pending", "sold"]},
        "category": {
            "type": "object",
            "properties": {
                "id":   {"type": "integer"},
                "name": {"type": "string"}
            }
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status"],
    "properties": {
        "id":       {"type": "integer"},
        "petId":    {"type": "integer"},
        "quantity": {"type": "integer", "minimum": 0},
        "status":   {"type": "string", "enum": ["placed", "approved", "delivered"]},
        "complete": {"type": "boolean"},
        "shipDate": {"type": "string"}
    }
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "username"],
    "properties": {
        "id":         {"type": "integer"},
        "username":   {"type": "string", "minLength": 1},
        "firstName":  {"type": "string"},
        "lastName":   {"type": "string"},
        "email":      {"type": "string"},
        "phone":      {"type": "string"},
        "userStatus": {"type": "integer"}
    }
}


# ------------------------------------------------------------------
# Assertion helpers
# ------------------------------------------------------------------

def assert_status(response, expected: int):
    """Assert HTTP status code with a clear failure message."""
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}.\n"
        f"URL: {response.url}\n"
        f"Body: {response.text[:500]}"
    )


def assert_schema(data: dict, schema: dict):
    """Validate a response dict against a JSON schema.

    Raises AssertionError with a clear message on schema violation.
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(
            f"Schema validation failed:\n"
            f"  Field: {' -> '.join(str(p) for p in e.absolute_path) or 'root'}\n"
            f"  Message: {e.message}"
        )


def assert_field_equals(response_body: dict, field: str, expected):
    """Assert a top-level field in the response body equals expected value."""
    actual = response_body.get(field)
    assert actual == expected, (
        f"Field '{field}': expected '{expected}', got '{actual}'."
    )


def assert_field_not_empty(response_body: dict, field: str):
    """Assert a top-level field exists and is not None / empty."""
    value = response_body.get(field)
    assert value is not None and value != "" and value != [], (
        f"Field '{field}' is empty or missing in response: {response_body}"
    )
