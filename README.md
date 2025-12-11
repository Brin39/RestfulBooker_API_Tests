# Restful Booker API Testing Framework

Comprehensive automated testing framework for the [Restful Booker API](https://restful-booker.herokuapp.com/) — a sample hotel booking API for practicing API testing.

## 🎯 Features

- **27 test cases** (30 test methods) covering all API operations
- **Clean architecture** with separation of concerns (infra/logic/tests)
- **Independent tests** — can run in parallel without conflicts
- **Test data generation** — unique data for each test run
- **Comprehensive coverage** — CRUD, authentication, validation, security, performance

## 📁 Project Structure

```
├── infra/                    # Infrastructure layer
│   └── base_api.py          # Base HTTP client
├── logic/                    # Business logic layer
│   ├── ping_api.py          # Health check API
│   ├── auth_api.py          # Authentication API
│   └── booking_api.py       # Booking CRUD API
├── tests/                    # Test layer
│   ├── conftest.py          # Shared fixtures
│   ├── test_ping.py         # Health check tests
│   ├── test_auth.py         # Authentication tests
│   ├── test_booking_crud.py # CRUD tests (T001-T005)
│   ├── test_booking_negative.py    # Negative tests (T008-T015)
│   ├── test_booking_validation.py  # Schema/headers tests (T016-T017)
│   ├── test_booking_performance.py # Performance tests (T019-T020)
│   ├── test_booking_concurrency.py # Concurrency tests (T021-T023)
│   └── test_booking_security.py    # Security tests (T024-T027)
├── utils/                    # Utilities
│   └── test_data.py         # Test data generators
├── pytest.ini               # Pytest configuration
└── requirements.txt         # Dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Brin39/RestfulBooker_API_Tests.git
cd RestfulBooker_API_Tests
```

2. Create virtual environment:
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🧪 Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_booking_crud.py -v
```

### Run with HTML report
```bash
pytest --html=report.html
```

### Run tests in parallel
```bash
pytest -n auto
```

## 📊 Test Coverage

| ID | Test Name | Category |
|----|-----------|----------|
| T001 | Create booking - successful creation | CRUD |
| T002 | Get booking by id | CRUD |
| T003 | Update booking (PUT) - full update | CRUD |
| T004 | Partial update (PATCH) | CRUD |
| T005 | Delete booking | CRUD |
| T006 | Auth - valid credentials | Auth |
| T007 | Auth - invalid credentials | Auth |
| T008 | Update without token | Negative |
| T009 | Delete without token | Negative |
| T010 | Create - empty required fields | Negative |
| T011 | Create - invalid dates | Negative |
| T012 | Create - very long strings | Negative |
| T013 | Create - minimal fields | Negative |
| T014 | Duplicates - different IDs | Negative |
| T015 | GET non-existent booking | Negative |
| T016 | JSON schema validation | Validation |
| T017 | Response headers | Validation |
| T018 | Ping/health check | Health |
| T019 | SLA - response time | Performance |
| T020 | Parallel creation | Performance |
| T021 | Concurrent updates | Concurrency |
| T022 | Concurrent delete + read | Concurrency |
| T023 | Teardown cleanup | Concurrency |
| T024 | XSS/injection check | Security |
| T025 | Malformed JSON | Security |
| T026 | Token not leaked | Security |
| T027 | Mass cleanup | Security |

## 🛠 Technologies

- **Python 3.12**
- **pytest** — testing framework
- **httpx** — HTTP client
- **pytest-xdist** — parallel test execution
- **pytest-html** — HTML reports

## 📝 API Documentation

- [Restful Booker API Docs](https://restful-booker.herokuapp.com/apidoc/index.html)

## 👤 Author

Created for API testing practice and learning.
