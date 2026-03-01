# Swagger Petstore — API Automation Roadmap 🗺️

**Target API:** https://petstore.swagger.io (v2) / https://petstore3.swagger.io (v3 OpenAPI 3.0)  
**Recommended Stack:** Python · Pytest · Requests · python-dotenv  
**Estimated Effort:** 4–6 weeks (part-time)

---

## Why This Project

The Swagger Petstore is the industry-standard public API used to demonstrate and practice API testing. It covers three real-world resource domains (Pet, Store, User), includes auth patterns (API key + OAuth), and has intentional edge-case behaviours baked in (e.g. ID > 5 throws an exception). This makes it an ideal portfolio project to sit alongside the SauceDemo UI framework.

---

## API Overview

Base URL: `https://petstore.swagger.io/v2`  
Auth: `api_key: special-key` (header) for protected endpoints

| Domain | Endpoints | Methods |
|---|---|---|
| **Pet** | `/pet`, `/pet/{petId}`, `/pet/findByStatus`, `/pet/findByTags`, `/pet/{petId}/uploadFile` | GET, POST, PUT, DELETE |
| **Store** | `/store/inventory`, `/store/order`, `/store/order/{orderId}` | GET, POST, DELETE |
| **User** | `/user`, `/user/login`, `/user/logout`, `/user/{username}` | GET, POST, PUT, DELETE |

---

## Recommended Project Structure

```
petstore-api-pytest/
│
├── src/
│   ├── config.py                  # Base URL, API key, env vars
│   ├── api/
│   │   ├── base_client.py         # Shared requests.Session, headers, response helpers
│   │   ├── pet_client.py          # All /pet endpoint calls
│   │   ├── store_client.py        # All /store endpoint calls
│   │   └── user_client.py         # All /user endpoint calls
│   └── utils/
│       ├── data_factory.py        # Random test data generators (fake pet names, etc.)
│       └── assertions.py          # Reusable response assertion helpers
│
├── tests/
│   ├── conftest.py                # Fixtures: session, clients, shared test data
│   ├── pet/
│   │   ├── test_pet_create.py     # POST /pet
│   │   ├── test_pet_read.py       # GET /pet/{petId}, findByStatus, findByTags
│   │   ├── test_pet_update.py     # PUT /pet, POST /pet/{petId}
│   │   └── test_pet_delete.py     # DELETE /pet/{petId}
│   ├── store/
│   │   ├── test_store_inventory.py
│   │   └── test_store_order.py
│   └── user/
│       ├── test_user_crud.py
│       └── test_user_auth.py
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Phase 1 — Project Setup (Week 1)

### Goals
Stand up the project skeleton, confirm connectivity to the API, and establish the patterns every test file will follow.

### Tasks

- [ ] Create the repo and virtual environment
- [ ] Install dependencies: `pytest`, `requests`, `python-dotenv`, `faker`, `pytest-html`
- [ ] Create `src/config.py` loading `BASE_URL` and `API_KEY` from `.env`
- [ ] Build `src/api/base_client.py` with a shared `requests.Session`, default headers (`Content-Type`, `api_key`), and a response validator helper
- [ ] Write a smoke test confirming `GET /pet/findByStatus?status=available` returns 200
- [ ] Set up `pytest.ini` with markers: `smoke`, `regression`, `negative`, `pet`, `store`, `user`
- [ ] Configure `pytest-html` for report generation

### Key Design Decision
Use a `BaseClient` class with a `requests.Session` rather than calling `requests.get()` directly in tests. This mirrors what you did with `BasePage` in the SauceDemo project — one place to set headers, timeouts, and base URL.

```python
# src/api/base_client.py sketch
class BaseClient:
    def __init__(self, base_url: str, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "api_key": api_key
        })
        self.base_url = base_url

    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)
    # ... put, delete
```

---

## Phase 2 — Pet Domain (Week 2)

The Pet domain is the richest and most important. Build and test it fully before moving on.

### Endpoints to Cover

#### `POST /pet` — Create a pet

| Test ID | Scenario | Expected |
|---|---|---|
| PET-C001 | Create pet with all valid fields | 200, pet returned with correct fields |
| PET-C002 | Create pet with required fields only (name, photoUrls) | 200, pet created |
| PET-C003 | Create pet with empty body | 405 Method Not Allowed |
| PET-C004 | Create pet with invalid JSON | 400 or 415 |
| PET-C005 | Create pet with status = available / pending / sold | 200 for each (parametrize) |

#### `GET /pet/{petId}` — Get pet by ID

| Test ID | Scenario | Expected |
|---|---|---|
| PET-R001 | Get pet with valid ID (just created) | 200, correct pet data |
| PET-R002 | Get pet with ID > 5 (Petstore quirk) | 404 or exception |
| PET-R003 | Get pet with ID = 0 | 404 |
| PET-R004 | Get pet with non-integer ID (e.g. "abc") | 400 |
| PET-R005 | Get pet with very large ID (e.g. 999999999) | 404 |

#### `GET /pet/findByStatus`

| Test ID | Scenario | Expected |
|---|---|---|
| PET-FS001 | findByStatus=available | 200, list of pets |
| PET-FS002 | findByStatus=pending | 200, list (may be empty) |
| PET-FS003 | findByStatus=sold | 200, list (may be empty) |
| PET-FS004 | Invalid status value | 400 |
| PET-FS005 | Response list items all have status=available | 200, schema validated |

#### `PUT /pet` — Update a pet

| Test ID | Scenario | Expected |
|---|---|---|
| PET-U001 | Update name of existing pet | 200, updated name returned |
| PET-U002 | Update status from available → sold | 200, status updated |
| PET-U003 | Update pet with non-existent ID | 404 |
| PET-U004 | Update with invalid fields | 400 |

#### `DELETE /pet/{petId}`

| Test ID | Scenario | Expected |
|---|---|---|
| PET-D001 | Delete existing pet | 200 |
| PET-D002 | Delete already-deleted pet | 404 |
| PET-D003 | Delete with invalid ID | 400 |
| PET-D004 | Verify pet is actually gone after delete (GET after DELETE) | 404 on subsequent GET |

### Data Factory Pattern

Use `faker` to generate unique test data per test run, avoiding ID collisions between runs:

```python
# src/utils/data_factory.py sketch
from faker import Faker
import random

fake = Faker()

def make_pet(status: str = "available") -> dict:
    return {
        "id": random.randint(100000, 999999),
        "name": fake.first_name(),
        "status": status,
        "photoUrls": ["https://example.com/photo.jpg"],
        "category": {"id": 1, "name": "Dogs"},
        "tags": [{"id": 1, "name": fake.word()}]
    }
```

---

## Phase 3 — Store Domain (Week 3)

### Endpoints to Cover

#### `GET /store/inventory`

| Test ID | Scenario | Expected |
|---|---|---|
| STR-I001 | Get inventory | 200, response is a dict of status → count |
| STR-I002 | Validate response schema (keys are strings, values are ints) | 200, schema valid |
| STR-I003 | Inventory changes after adding a pet with status=sold | Count for "sold" increases by 1 |

#### `POST /store/order` — Place an order

| Test ID | Scenario | Expected |
|---|---|---|
| STR-O001 | Place order for existing pet | 200, order returned with id |
| STR-O002 | Place order with status=placed / approved / delivered (parametrize) | 200 each |
| STR-O003 | Place order with invalid petId | 400 |
| STR-O004 | Place order with quantity = 0 | 400 or 200 depending on API behaviour |
| STR-O005 | Place order with empty body | 400 |

#### `GET /store/order/{orderId}`

| Test ID | Scenario | Expected |
|---|---|---|
| STR-O006 | Get order just placed | 200, correct order data |
| STR-O007 | Get order with ID > 10 (Petstore quirk throws exception) | 404 |
| STR-O008 | Get deleted order | 404 |

#### `DELETE /store/order/{orderId}`

| Test ID | Scenario | Expected |
|---|---|---|
| STR-O009 | Delete valid order | 200 |
| STR-O010 | Delete non-existent order | 404 |
| STR-O011 | Verify order is gone after delete | 404 on subsequent GET |

---

## Phase 4 — User Domain (Week 4)

### Endpoints to Cover

#### `POST /user` — Create user

| Test ID | Scenario | Expected |
|---|---|---|
| USR-C001 | Create user with all fields | 200 |
| USR-C002 | Create user with minimum required fields | 200 |
| USR-C003 | Create user with duplicate username | API-dependent (test and document behaviour) |

#### `GET /user/login` and `GET /user/logout`

| Test ID | Scenario | Expected |
|---|---|---|
| USR-A001 | Login with valid username + password | 200, session token in response |
| USR-A002 | Login with invalid credentials | 400 |
| USR-A003 | Login with empty credentials | 400 |
| USR-A004 | Logout after login | 200 |
| USR-A005 | Logout without login | Document behaviour (may return 200) |

#### `GET /user/{username}`

| Test ID | Scenario | Expected |
|---|---|---|
| USR-R001 | Get existing user | 200, correct user data |
| USR-R002 | Get non-existent user | 404 |
| USR-R003 | Validate response schema matches creation payload | 200, all fields present |

#### `PUT /user/{username}` and `DELETE /user/{username}`

| Test ID | Scenario | Expected |
|---|---|---|
| USR-U001 | Update user email | 200, updated |
| USR-U002 | Update non-existent user | 404 |
| USR-D001 | Delete existing user | 200 |
| USR-D002 | Delete non-existent user | 404 |
| USR-D003 | GET after DELETE confirms user is gone | 404 |

---

## Phase 5 — Advanced & Cross-Domain (Week 5)

### End-to-End Flow Tests

These chain multiple API calls together, mirroring how real users interact with the system. Add a `tests/e2e/` folder for these.

| Test ID | Flow | Steps |
|---|---|---|
| E2E-001 | Full pet lifecycle | Create pet → GET by ID → Update status → DELETE → verify gone |
| E2E-002 | Full order lifecycle | Create pet → Place order → GET order → DELETE order → verify gone |
| E2E-003 | Full user lifecycle | Create user → Login → GET user → Update → DELETE → verify gone |
| E2E-004 | Inventory reflects pet status | Create pet (available) → check inventory count → update to sold → check inventory again |

### Schema Validation

Add `jsonschema` to validate response bodies structurally, not just by status code:

```python
# Example: validate a Pet response
PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls", "status"],
    "properties": {
        "id":        {"type": "integer"},
        "name":      {"type": "string"},
        "status":    {"type": "string", "enum": ["available", "pending", "sold"]},
        "photoUrls": {"type": "array", "items": {"type": "string"}}
    }
}
```

### Performance Baseline (Optional)

Add `pytest-benchmark` to record response time baselines for key endpoints:

| Endpoint | Acceptable p95 |
|---|---|
| GET /pet/findByStatus | < 2000ms |
| POST /pet | < 2000ms |
| GET /store/inventory | < 2000ms |

---

## Phase 6 — Polish & CI (Week 6)

- [ ] Add `pytest-html` HTML report generation to `pytest.ini`
- [ ] Add a GitHub Actions workflow (`.github/workflows/api-tests.yml`) to run on push
- [ ] Add a `Makefile` with `make test`, `make smoke`, `make report` shortcuts
- [ ] Write the README with setup instructions, endpoint coverage table, and how to run
- [ ] Add `requirements.txt` with all pinned versions

### GitHub Actions Example

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -m smoke --html=report.html
      - uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: report.html
```

---

## Markers Plan

```ini
[pytest]
addopts = -v -s
markers =
    smoke: Critical path tests
    regression: Full regression suite
    negative: Invalid input and error handling
    pet: Pet domain tests
    store: Store domain tests
    user: User domain tests
    e2e: End-to-end flow tests
    schema: Schema validation tests
```

---

## Key Differences vs the SauceDemo UI Project

| Concern | SauceDemo (UI) | Petstore (API) |
|---|---|---|
| What you're testing | Browser rendering + user flows | HTTP contracts + data integrity |
| Speed | Slow (seconds per test) | Fast (milliseconds per test) |
| Flakiness source | DOM timing, browser state | Network, shared server state |
| Main assertion | Element visibility, text, navigation | Status codes, response body, schema |
| State management | Fixtures log in/out, clear cart | Fixtures create/delete resources |
| Parallelism | Hard (shared browser) | Easy (`pytest-xdist -n auto`) |

---

## Recommended Dependencies

```
pytest==8.3.5
requests==2.32.3
python-dotenv==1.0.1
faker==24.0.0
jsonschema==4.21.1
pytest-html==4.1.1
pytest-xdist==3.5.0
```
