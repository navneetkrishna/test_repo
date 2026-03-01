# Swagger Petstore API Automation Framework 🐾

A professional API automation framework for the [Swagger Petstore](https://petstore.swagger.io) built with **Python**, **Pytest**, and **Requests**, following the same architectural patterns as the [SauceDemo UI framework](https://github.com/navneetkrishna/saucedemo-selenium-pytest).

---

## 📋 Table of Contents

- [About](#about)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Clients](#api-clients)
- [Test Suites](#test-suites)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Test Markers](#test-markers)
- [Framework Design](#framework-design)

---

## About

This framework automates the Swagger Petstore REST API across three domains — **Pet**, **Store**, and **User** — covering happy path, negative, schema validation, and end-to-end lifecycle tests.

It is intentionally designed to mirror the SauceDemo UI project:

| Concept | UI Framework | API Framework |
|---|---|---|
| Base abstraction | `BasePage` | `BaseClient` |
| Domain objects | Page Objects | API Clients |
| Shared helpers | `waits.py` | `assertions.py` |
| Test data | Hardcoded strings | `data_factory.py` (Faker) |
| State management | `app_login`, `clean_cart` fixtures | `created_pet`, `created_order`, `created_user` fixtures |
| Config | `config.py` + `.env` | `config.py` + `.env` |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Primary language |
| Requests 2.32 | HTTP client |
| Pytest 8.3 | Test runner and fixture framework |
| Faker 24.0 | Random test data generation |
| jsonschema 4.21 | Response body schema validation |
| pytest-html 4.1 | HTML test reports |
| python-dotenv 1.0 | Environment variable management |

---

## Project Structure

```
petstore-api-pytest/
│
├── src/
│   ├── config.py                        # Base URL and API key from .env
│   ├── api/
│   │   ├── base_client.py               # Shared Session, headers, HTTP verbs
│   │   ├── pet_client.py                # /pet endpoint methods
│   │   ├── store_client.py              # /store endpoint methods
│   │   └── user_client.py               # /user endpoint methods
│   └── utils/
│       ├── data_factory.py              # Faker-based payload generators
│       └── assertions.py                # Reusable assert helpers + JSON schemas
│
├── tests/
│   ├── conftest.py                      # Session clients + resource fixtures
│   ├── api/
│   │   ├── pet/
│   │   │   ├── test_pet_create.py       # POST /pet (PET-C001–005)
│   │   │   ├── test_pet_read.py         # GET /pet (PET-R001–008)
│   │   │   ├── test_pet_update.py       # PUT /pet (PET-U001–005)
│   │   │   └── test_pet_delete.py       # DELETE /pet (PET-D001–004)
│   │   ├── store/
│   │   │   ├── test_store_inventory.py  # GET /store/inventory (STR-I001–003)
│   │   │   └── test_store_order.py      # /store/order CRUD (STR-O001–010)
│   │   ├── user/
│   │   │   ├── test_user_crud.py        # /user CRUD (USR-C001–USR-D003)
│   │   │   └── test_user_auth.py        # /user/login + logout (USR-A001–006)
│   │   └── e2e/
│   │       ├── test_pet_lifecycle.py    # Full pet Create→Read→Update→Delete flow
│   │       ├── test_order_lifecycle.py  # Full order flow including inventory check
│   │       └── test_user_lifecycle.py   # Full user flow including batch creation
│
├── reports/                             # Auto-created HTML reports
├── .env.example                         # Template — copy to .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## API Clients

Each client inherits from `BaseClient` and wraps a specific domain's endpoints.

| Client | Base Path | Methods |
|---|---|---|
| `PetClient` | `/pet` | `create_pet`, `get_pet_by_id`, `find_by_status`, `find_by_tags`, `update_pet`, `update_pet_form`, `delete_pet` |
| `StoreClient` | `/store` | `get_inventory`, `place_order`, `get_order_by_id`, `delete_order` |
| `UserClient` | `/user` | `create_user`, `create_users_with_list`, `login`, `logout`, `get_user`, `update_user`, `delete_user` |

---

## Test Suites

### 🐶 Pet Domain

| Test ID | Description | Markers |
|---|---|---|
| PET-C001 | Create pet with all fields | smoke, regression, pet |
| PET-C002 | Create pet with minimum fields | smoke, regression, pet |
| PET-C003 | Create pet for each status (parametrized) | regression, pet |
| PET-C004 | Create with empty body — expect 4xx | negative, regression, pet |
| PET-C005 | Create with invalid JSON — expect 4xx | negative, regression, pet |
| PET-R001 | GET by valid ID | smoke, regression, pet |
| PET-R002 | GET by non-existent ID — expect 404 | negative, regression, pet |
| PET-R003 | GET by ID=0 — expect 400/404 | negative, regression, pet |
| PET-R004 | GET by negative ID — expect 4xx | negative, regression, pet |
| PET-R005 | Response schema validation | schema, regression, pet |
| PET-R006 | findByStatus for each status (parametrized) | smoke, regression, pet |
| PET-R007 | findByStatus items all match requested status | regression, pet |
| PET-R008 | findByStatus with invalid status | negative, regression, pet |
| PET-U001 | Update pet name via PUT | smoke, regression, pet |
| PET-U002 | Update status to sold via PUT | regression, pet |
| PET-U003 | Update non-existent pet | negative, regression, pet |
| PET-U004 | PUT with empty body — expect 4xx | negative, regression, pet |
| PET-U005 | Update via form data | regression, pet |
| PET-D001 | Delete existing pet | smoke, regression, pet |
| PET-D002 | Delete already-deleted pet | regression, pet |
| PET-D003 | Delete non-existent pet | negative, regression, pet |
| PET-D004 | DELETE then verify 404 on subsequent GET | regression, pet |

### 🏪 Store Domain

| Test ID | Description | Markers |
|---|---|---|
| STR-I001 | GET inventory returns 200 and dict | smoke, regression, store |
| STR-I002 | Inventory schema: string keys, int values | schema, regression, store |
| STR-I003 | Adding sold pet increments sold count | regression, store |
| STR-O001 | Place valid order | smoke, regression, store |
| STR-O002 | Place order for each status (parametrized) | regression, store |
| STR-O003 | Place order with empty body — 4xx | negative, regression, store |
| STR-O004 | Place order with quantity=0 | negative, regression, store |
| STR-O005 | GET order by ID | smoke, regression, store |
| STR-O006 | GET order with invalid ID | negative, regression, store |
| STR-O007 | GET deleted order — expect 404 | regression, store |
| STR-O008 | DELETE order | regression, store |
| STR-O009 | DELETE non-existent order | negative, regression, store |
| STR-O010 | Order response schema validation | schema, regression, store |

### 👤 User Domain

| Test ID | Description | Markers |
|---|---|---|
| USR-C001 | Create user with all fields | smoke, regression, user |
| USR-C002 | Create user with minimum fields | regression, user |
| USR-C003 | Create user with empty body | negative, regression, user |
| USR-R001 | GET existing user | smoke, regression, user |
| USR-R002 | GET non-existent user — 404 | negative, regression, user |
| USR-R003 | GET user schema validation | schema, regression, user |
| USR-R004 | GET user fields match creation payload | regression, user |
| USR-U001 | Update user email | regression, user |
| USR-U002 | Update non-existent user | negative, regression, user |
| USR-D001 | Delete existing user | regression, user |
| USR-D002 | Delete non-existent user | negative, regression, user |
| USR-D003 | DELETE then verify 404 | regression, user |
| USR-A001 | Login with valid credentials | smoke, regression, user |
| USR-A002 | Login with invalid credentials | negative, regression, user |
| USR-A003 | Login with empty credentials | negative, regression, user |
| USR-A004 | Logout after login | smoke, regression, user |
| USR-A005 | Logout without prior login | regression, user |
| USR-A006 | Login response includes X-Expires-After header | regression, user |

### 🔄 End-to-End Flows

| Test ID | Description | Markers |
|---|---|---|
| E2E-PET-001 | Full pet lifecycle: Create → Read → Update → Delete → Verify | smoke, regression, e2e, pet |
| E2E-PET-002 | Created pet appears in findByStatus results | regression, e2e, pet |
| E2E-ORD-001 | Full order lifecycle: Create pet → Order → Read → Cancel → Verify | smoke, regression, e2e, store |
| E2E-ORD-002 | Sold pet increments inventory sold count | regression, e2e, store |
| E2E-USR-001 | Full user lifecycle: Create → Login → Read → Update → Logout → Delete | smoke, regression, e2e, user |
| E2E-USR-002 | Batch create users; all are retrievable | regression, e2e, user |

---

## Getting Started

### Prerequisites

- Python 3.11 or higher

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/navneetkrishna/petstore-api-pytest.git
cd petstore-api-pytest

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env
```

### Configuration

`.env` file:

```env
BASE_URL=https://petstore.swagger.io/v2
API_KEY=special-key
```

The framework works out of the box with the defaults — no changes needed unless targeting a different environment.

---

## Running Tests

```bash
# All tests
pytest

# Smoke tests only
pytest -m smoke

# Full regression
pytest -m regression

# By domain
pytest -m pet
pytest -m store
pytest -m user
pytest -m e2e

# Negative tests only
pytest -m negative

# Schema validation only
pytest -m schema

# Single file
pytest tests/api/pet/test_pet_create.py

# Single test
pytest tests/api/e2e/test_pet_lifecycle.py::TestPetLifecycle::test_e2e_pet_001_full_lifecycle

# With HTML report
pytest --html=reports/report.html
```

---

## Test Markers

| Marker | Description |
|---|---|
| `smoke` | Critical path — run first |
| `regression` | Full suite |
| `negative` | Invalid inputs and error paths |
| `schema` | JSON schema validation tests |
| `e2e` | Multi-step lifecycle flows |
| `pet` | Pet domain |
| `store` | Store domain |
| `user` | User domain |

---

## Framework Design

### BaseClient

`src/api/base_client.py` is the foundation every API client inherits from — mirroring what `BasePage` does in the UI framework.

- Owns the `requests.Session` with default headers (`Content-Type`, `Accept`, `api_key`)
- Provides `get()`, `post()`, `put()`, `delete()` with base URL prepended and timeout applied
- Provides `json()` helper that parses the response and raises a clear error on invalid JSON
- Provides `is_success()` for quick 2xx check

### Fixture Hierarchy

```
pet_client, store_client, user_client  (session scope — one instance per run)
└── created_pet     (function scope — fresh pet per test, deleted after)
    └── created_order (function scope — depends on created_pet)
└── created_user    (function scope — fresh user per test, deleted after)
```

Every resource fixture creates the resource before the test and deletes it in teardown — even if the test itself fails. This guarantees no orphaned data is left on the server between runs.

### Data Factory

`src/utils/data_factory.py` uses `faker` to generate unique, realistic payloads per test run:

- `make_pet(status)` — random ID, name, category, tags, photoUrls
- `make_order(pet_id, quantity, status)` — valid order within Petstore's accepted ID range
- `make_user(username)` — random username, name, email, phone, password

Random IDs in the range `100_000–999_999` are used for pets and users to minimise collision with data left by other test runners on the shared Petstore instance.

### Assertions

`src/utils/assertions.py` provides four reusable helpers used across all test files:

| Helper | Purpose |
|---|---|
| `assert_status(response, expected)` | Status code check with URL and body in the failure message |
| `assert_schema(data, schema)` | jsonschema validation with a readable field-level failure message |
| `assert_field_equals(body, field, expected)` | Top-level field value check |
| `assert_field_not_empty(body, field)` | Field presence and non-empty check |
